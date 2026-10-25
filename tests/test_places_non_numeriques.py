import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def reserver(places):
    client = client_connecte("Iron Temple")
    return client.post("/purchasePlaces", data={
        "club": "Iron Temple",          # 4 points
        "competition": "Spring Festival",
        "places": places,
    })

def test_reservation_refusee_avec_un_champ_vide():
    # Cas réel : le secrétaire clique sur Book sans rien saisir
    response = reserver("")
    assert response.status_code == 200          # pas d'erreur 500
    assert b"Desole veuillez entrer un nombre de places valide" in response.data

def test_reservation_refusee_avec_du_texte():
    competition = trouver(server.competitions, "Spring Festival")
    response = reserver("abc")
    club = trouver(server.clubs, "Iron Temple")
    assert response.status_code == 200
    assert b"Desole veuillez entrer un nombre de places valide" in response.data
    assert int(club['points']) == 4
    assert int(competition['numberOfPlaces']) == 25
