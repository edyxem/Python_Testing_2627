import server
from outils import client_connecte

FORMULAIRE = b"How many places?"

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def ouvrir_page_reservation():
    client = client_connecte("Simply Lift")
    return client.get("/book/Spring Festival/Simply Lift")

def test_page_reservation_refusee_pour_une_competition_passee():
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    response = ouvrir_page_reservation()
    assert response.status_code == 200
    assert b"Desole cette competition est deja passee" in response.data
    assert FORMULAIRE not in response.data

def test_page_reservation_refusee_pour_une_competition_complete():
    competition = trouver(server.competitions, "Spring Festival")
    competition['date'] = "2999-03-27 10:00:00"
    competition['numberOfPlaces'] = "0"
    response = ouvrir_page_reservation()
    assert response.status_code == 200
    assert b"Desole cette competition est complete" in response.data
    assert FORMULAIRE not in response.data

def test_page_reservation_affichee_pour_une_competition_disponible():
    # Non-régression : compétition future avec des places, le formulaire s'affiche
    trouver(server.competitions, "Spring Festival")['date'] = "2999-03-27 10:00:00"
    response = ouvrir_page_reservation()
    assert response.status_code == 200
    assert FORMULAIRE in response.data
