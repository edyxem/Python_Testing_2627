import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def test_reservation_refusee_si_pas_assez_de_places():
    client = client_connecte("Simply Lift")
    competition = trouver(server.competitions, "Fall Classic")
    competition['numberOfPlaces'] = "2"   # la compétition est presque complète
    club = trouver(server.clubs, "Simply Lift")                      # 13 points
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Fall Classic",
        "places": "3",                  # assez de points, moins de 12, mais plus que les places restantes
    })
    assert response.status_code == 200
    assert b"Desole pas assez de places disponibles" in response.data
    assert int(competition['numberOfPlaces']) == 2
    assert int(club['points']) == 13

def test_reservation_acceptee_avec_les_dernieres_places():
    # Valeur limite : réserver exactement les places restantes doit fonctionner
    client = client_connecte("Simply Lift")
    competition = trouver(server.competitions, "Fall Classic")
    competition['numberOfPlaces'] = "2"
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Fall Classic",
        "places": "2",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Reservation confirmee" in response.data
    assert int(competition['numberOfPlaces']) == 0
