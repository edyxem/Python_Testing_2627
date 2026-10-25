import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

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

def test_tableau_a_jour_apres_une_reservation():
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    client = client_connecte("Simply Lift")         # 13 points
    client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "2",
    })
    response = server.app.test_client().get("/tableau-points")   # visiteur non connecté
    assert b"<td>11</td>" in response.data
    assert b"<td>13</td>" not in response.data

def test_tableau_en_lecture_seule():
    # La spécification demande un tableau en lecture seule : pas d'envoi de données
    client = server.app.test_client()
    response = client.post("/tableau-points")
    assert response.status_code == 405

def test_lien_vers_le_tableau_depuis_l_accueil():
    client = server.app.test_client()
    response = client.get("/")
    assert b'href="/tableau-points"' in response.data
