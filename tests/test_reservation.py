import server
from outils import client_connecte

def test_reservation_refusee_si_points_insuffisants():
    client = client_connecte("Iron Temple")
    competition = [c for c in server.competitions if c['name'] == "Spring Festival"][0]
    places_avant = int(competition['numberOfPlaces'])
    response = client.post("/purchasePlaces", data={
        "club": "Iron Temple",          # le club qui a 4 points
        "competition": "Spring Festival",
        "places": "5",                  # plus que ses points
    })
    assert response.status_code == 200
    assert b"Desole pas assez de points" in response.data
    assert int(competition['numberOfPlaces']) == places_avant

def test_points_deduits_apres_reservation():
    client = client_connecte("Simply Lift")
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",          # le club qui a 13 points
        "competition": "Spring Festival",
        "places": "2",
    })
    club = [c for c in server.clubs if c['name'] == "Simply Lift"][0]
    assert response.status_code == 200
    assert int(club['points']) == 11                 # 13 - 2
    assert b"Points available: 11" in response.data
