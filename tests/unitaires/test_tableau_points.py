import server

def test_tableau_accessible_sans_connexion():
    client = server.app.test_client()
    response = client.get("/tableau-points")
    assert response.status_code == 200

def test_tableau_affiche_tous_les_clubs_avec_leurs_points():
    client = server.app.test_client()
    response = client.get("/tableau-points")
    for club in server.clubs:
        assert ("<td>" + club['name'] + "</td>").encode() in response.data
        assert ("<td>" + str(club['points']) + "</td>").encode() in response.data

def test_tableau_en_lecture_seule():
    # La spécification demande un tableau en lecture seule : pas d'envoi de données
    client = server.app.test_client()
    response = client.post("/tableau-points")
    assert response.status_code == 405

def test_lien_vers_le_tableau_depuis_l_accueil():
    client = server.app.test_client()
    response = client.get("/")
    assert b'href="/tableau-points"' in response.data
