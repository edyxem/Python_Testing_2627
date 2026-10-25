import server

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def reserver(places):
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    client = server.app.test_client()
    return client.post("/purchasePlaces", data={
        "club": "Simply Lift",          # 13 points
        "competition": "Spring Festival",
        "places": places,
    })

def test_message_confirmation_indique_le_nombre_de_places():
    response = reserver("3")
    assert response.status_code == 200
    assert b"Reservation confirmee : 3 places achetees" in response.data

def test_message_confirmation_au_singulier_pour_une_place():
    response = reserver("1")
    assert response.status_code == 200
    assert b"Reservation confirmee : 1 place achetee" in response.data
