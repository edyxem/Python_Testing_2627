import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def reserver(client, suivre_redirection):
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    return client.post("/purchasePlaces", data={
        "club": "Simply Lift",          # 13 points
        "competition": "Spring Festival",
        "places": "2",
    }, follow_redirects=suivre_redirection)

def test_achat_reussi_redirige_vers_une_page_en_get():
    # Post/Redirect/Get : après un achat, le serveur redirige au lieu d'afficher la page
    client = client_connecte("Simply Lift")
    response = reserver(client, False)
    assert response.status_code == 302

def test_page_apres_redirection_affiche_la_confirmation():
    client = client_connecte("Simply Lift")
    response = reserver(client, True)
    assert response.status_code == 200
    assert b"Reservation confirmee : 2 places achetees" in response.data
    assert b"Points available: 11" in response.data

def test_actualiser_la_page_ne_reserve_pas_une_deuxieme_fois():
    # Actualiser (F5) = refaire la dernière requête de la page affichée
    client = client_connecte("Simply Lift")
    response = reserver(client, True)
    actualisation = client.get(response.request.path)
    assert actualisation.status_code == 200
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 11     # pas 9
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 23
