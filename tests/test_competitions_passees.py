import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def test_reservation_refusee_pour_une_competition_passee():
    client = client_connecte("Simply Lift")
    competition = trouver(server.competitions, "Spring Festival")
    competition['date'] = "2020-03-27 10:00:00"      # date dans le passé
    places_avant = int(competition['numberOfPlaces'])
    club = trouver(server.clubs, "Simply Lift")       # 13 points
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "1",
    })
    assert response.status_code == 200
    assert b"Desole cette competition est deja passee" in response.data
    assert int(competition['numberOfPlaces']) == places_avant
    assert int(club['points']) == 13

def test_reservation_acceptee_pour_une_competition_future():
    # Date fixée loin dans le futur pour que le test reste valable dans le temps
    client = client_connecte("Simply Lift")
    competition = trouver(server.competitions, "Spring Festival")
    competition['date'] = "2999-03-27 10:00:00"
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "1",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Reservation confirmee" in response.data

def test_pas_de_lien_de_reservation_pour_une_competition_passee():
    client = server.app.test_client()
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    trouver(server.competitions, "Fall Classic")['date'] = "2999-10-22 13:30:00"
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"/book/Spring%20Festival/Simply%20Lift" not in response.data
    assert b"/book/Fall%20Classic/Simply%20Lift" in response.data   # à venir
