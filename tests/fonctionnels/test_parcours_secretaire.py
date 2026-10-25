import server

# Parcours complets d'un utilisateur, du début à la fin, comme dans l'exemple de
# parcours de la spécification. On ne touche pas aux données directement : tout
# passe par les pages et les formulaires, et on vérifie que chaque lien existe
# sur la page avant de le "cliquer".

def test_parcours_complet_d_une_reservation():
    client = server.app.test_client()

    # 1. Le secrétaire arrive sur l'accueil et se connecte avec son email
    accueil = client.get("/")
    assert b'action="showSummary"' in accueil.data
    resume = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"Bienvenue, john@simplylift.co" in resume.data
    assert b"Points disponibles : 13" in resume.data

    # 2. Il clique sur une compétition à venir
    assert b"/book/Spring%20Festival/Simply%20Lift" in resume.data
    formulaire = client.get("/book/Spring Festival/Simply Lift")
    assert b"Combien de places ?" in formulaire.data

    # 3. Il achète 3 places et voit la confirmation, ses points sont déduits
    confirmation = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "3",
    }, follow_redirects=True)
    assert b"Reservation confirmee : 3 places achetees" in confirmation.data
    assert b"Points disponibles : 10" in confirmation.data

    # 4. Il retrouve sa réservation dans "Mes reservations"
    assert b'href="/mes-reservations"' in confirmation.data
    mesReservations = client.get("/mes-reservations")
    assert b"<td>Spring Festival</td>" in mesReservations.data
    assert b"<td>3</td>" in mesReservations.data

    # 5. Il se déconnecte et ne peut plus réserver
    client.get("/logout")
    refus = client.get("/book/Spring Festival/Simply Lift")
    assert b"Desole vous devez etre connecte avec ce club" in refus.data

def test_parcours_avec_une_erreur_puis_une_correction():
    client = server.app.test_client()
    client.post("/showSummary", data={"email": "admin@irontemple.com"})     # 4 points

    # Il demande plus de places que ses points : erreur, rien n'est retiré
    erreur = client.post("/purchasePlaces", data={
        "club": "Iron Temple",
        "competition": "Fall Classic",
        "places": "5",
    }, follow_redirects=True)
    assert b"Desole pas assez de points" in erreur.data
    assert b"Points disponibles : 4" in erreur.data

    # Il corrige sa demande : la réservation passe
    correction = client.post("/purchasePlaces", data={
        "club": "Iron Temple",
        "competition": "Fall Classic",
        "places": "4",
    }, follow_redirects=True)
    assert b"Reservation confirmee : 4 places achetees" in correction.data
    assert b"Points disponibles : 0" in correction.data

def test_parcours_d_un_visiteur_qui_consulte_le_tableau():
    client = server.app.test_client()
    accueil = client.get("/")
    assert b'href="/tableau-points"' in accueil.data
    tableau = client.get("/tableau-points")
    assert tableau.status_code == 200
    assert b"<td>Simply Lift</td>" in tableau.data
    assert b"<td>Iron Temple</td>" in tableau.data
    assert b"<td>She Lifts</td>" in tableau.data
