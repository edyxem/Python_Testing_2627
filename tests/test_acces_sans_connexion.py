import server

MESSAGE = b"Desole vous devez etre connecte avec ce club"

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def connecter(client, email):
    return client.post("/showSummary", data={"email": email})

def reserver(client, club):
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    return client.post("/purchasePlaces", data={
        "club": club,
        "competition": "Spring Festival",
        "places": "2",
    }, follow_redirects=True)

def test_achat_refuse_sans_connexion():
    client = server.app.test_client()
    response = reserver(client, "Simply Lift")
    assert response.status_code == 200
    assert MESSAGE in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13

def test_page_reservation_refusee_sans_connexion():
    client = server.app.test_client()
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200
    assert MESSAGE in response.data
    assert b"How many places?" not in response.data

def test_achat_refuse_pour_un_autre_club():
    # Connecté en tant que Iron Temple, on essaie de dépenser les points de Simply Lift
    client = server.app.test_client()
    connecter(client, "admin@irontemple.com")
    response = reserver(client, "Simply Lift")
    assert MESSAGE in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13

def test_achat_accepte_une_fois_connecte():
    client = server.app.test_client()
    connecter(client, "john@simplylift.co")
    response = reserver(client, "Simply Lift")
    assert b"Reservation confirmee" in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 11

def test_achat_refuse_apres_deconnexion():
    client = server.app.test_client()
    connecter(client, "john@simplylift.co")
    client.get("/logout")
    response = reserver(client, "Simply Lift")
    assert MESSAGE in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13
