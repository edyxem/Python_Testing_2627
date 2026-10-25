import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def test_reservation_refusee_si_plus_de_12_places():
    client = client_connecte("Simply Lift")
    competition = trouver(server.competitions, "Spring Festival")   # 25 places
    club = trouver(server.clubs, "Simply Lift")                      # 13 points
    places_avant = int(competition['numberOfPlaces'])
    points_avant = int(club['points'])
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "13",                 # assez de points et de places, mais plus de 12
    })
    assert response.status_code == 200
    assert b"Desole maximum 12 places par competition" in response.data
    assert int(competition['numberOfPlaces']) == places_avant
    assert int(club['points']) == points_avant

def test_reservation_acceptee_avec_exactement_12_places():
    # Valeur limite : 12 places doit rester autorisé
    client = client_connecte("Simply Lift")
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "12",
    }, follow_redirects=True)
    competition = trouver(server.competitions, "Spring Festival")
    assert response.status_code == 200
    assert b"Reservation confirmee" in response.data
    assert int(competition['numberOfPlaces']) == 13    # 25 - 12
