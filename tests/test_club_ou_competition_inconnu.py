import server
from outils import client_connecte

MESSAGE = b"Desole club ou competition introuvable"

def test_page_reservation_avec_competition_inconnue():
    client = server.app.test_client()
    response = client.get("/book/Competition Inconnue/Simply Lift")
    assert response.status_code == 200          # pas d'erreur 500
    assert MESSAGE in response.data

def test_page_reservation_avec_club_inconnu():
    client = server.app.test_client()
    response = client.get("/book/Spring Festival/Club Inconnu")
    assert response.status_code == 200
    assert MESSAGE in response.data

def test_page_reservation_valide_toujours_accessible():
    # Non-régression : un club et une compétition existants affichent le formulaire
    client = client_connecte("Simply Lift")
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200
    assert b"How many places?" in response.data

def test_achat_avec_competition_inconnue():
    client = server.app.test_client()
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Competition Inconnue",
        "places": "1",
    })
    assert response.status_code == 200
    assert MESSAGE in response.data

def test_achat_avec_club_inconnu():
    client = server.app.test_client()
    response = client.post("/purchasePlaces", data={
        "club": "Club Inconnu",
        "competition": "Spring Festival",
        "places": "1",
    })
    assert response.status_code == 200
    assert MESSAGE in response.data
