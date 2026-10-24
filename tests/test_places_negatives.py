import server

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def reserver(places):
    client = server.app.test_client()
    return client.post("/purchasePlaces", data={
        "club": "Iron Temple",          # 4 points
        "competition": "Spring Festival",
        "places": places,
    })

def test_reservation_refusee_avec_un_nombre_de_places_negatif():
    competition = trouver(server.competitions, "Spring Festival")
    competition['date'] = "2999-03-27 10:00:00"
    response = reserver("-5")
    club = trouver(server.clubs, "Iron Temple")
    assert response.status_code == 200
    assert b"Desole le nombre de places doit etre positif" in response.data
    assert int(club['points']) == 4                     # le club ne doit pas gagner de points
    assert int(competition['numberOfPlaces']) == 25     # la compétition ne doit pas gagner de places

def test_reservation_refusee_avec_zero_place():
    competition = trouver(server.competitions, "Spring Festival")
    competition['date'] = "2999-03-27 10:00:00"
    response = reserver("0")
    assert response.status_code == 200
    assert b"Desole le nombre de places doit etre positif" in response.data
