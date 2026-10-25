import server
from outils import trouver, client_connecte

# Tests de la page /book/<competition>/<club> (formulaire de réservation)

FORMULAIRE = b"How many places?"

def ouvrir_page_reservation(client):
    return client.get("/book/Spring Festival/Simply Lift")

def test_page_reservation_affichee_pour_une_competition_disponible():
    response = ouvrir_page_reservation(client_connecte("Simply Lift"))
    assert response.status_code == 200
    assert FORMULAIRE in response.data

def test_page_reservation_avec_competition_inconnue():
    client = server.app.test_client()
    response = client.get("/book/Competition Inconnue/Simply Lift")
    assert response.status_code == 200          # pas d'erreur 500
    assert b"Desole club ou competition introuvable" in response.data

def test_page_reservation_avec_club_inconnu():
    client = server.app.test_client()
    response = client.get("/book/Spring Festival/Club Inconnu")
    assert response.status_code == 200
    assert b"Desole club ou competition introuvable" in response.data

def test_page_reservation_refusee_sans_connexion():
    response = ouvrir_page_reservation(server.app.test_client())
    assert response.status_code == 200
    assert b"Desole vous devez etre connecte avec ce club" in response.data
    assert FORMULAIRE not in response.data

def test_page_reservation_refusee_pour_une_competition_passee():
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    response = ouvrir_page_reservation(client_connecte("Simply Lift"))
    assert response.status_code == 200
    assert b"Desole cette competition est deja passee" in response.data
    assert FORMULAIRE not in response.data

def test_page_reservation_refusee_pour_une_competition_complete():
    trouver(server.competitions, "Spring Festival")['numberOfPlaces'] = "0"
    response = ouvrir_page_reservation(client_connecte("Simply Lift"))
    assert response.status_code == 200
    assert b"Desole cette competition est complete" in response.data
    assert FORMULAIRE not in response.data
