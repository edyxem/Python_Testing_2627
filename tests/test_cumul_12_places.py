import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def reserver(client, places):
    return client.post("/purchasePlaces", data={
        "club": "Simply Lift",          # 13 points
        "competition": "Spring Festival",
        "places": places,
    }, follow_redirects=True)

def test_cumul_de_reservations_refuse_au_dela_de_12_places():
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    client = client_connecte("Simply Lift")
    reserver(client, "8")
    response = reserver(client, "5")                 # 8 + 5 = 13 places au total
    competition = trouver(server.competitions, "Spring Festival")
    assert response.status_code == 200
    assert b"Desole maximum 12 places par competition" in response.data
    assert int(competition['numberOfPlaces']) == 17  # 25 - 8 : la 2e réservation n'a rien retiré

def test_cumul_de_reservations_accepte_jusqu_a_12_places():
    # Valeur limite : 8 + 4 = 12 places au total doit être accepté
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    client = client_connecte("Simply Lift")
    reserver(client, "8")
    response = reserver(client, "4")
    assert response.status_code == 200
    assert b"Reservation confirmee" in response.data
