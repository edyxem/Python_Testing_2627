import server
from outils import trouver, client_connecte

# Tests de la page de résumé du club (/resume), celle affichée après le login


def test_resume_refuse_sans_connexion():
    client = server.app.test_client()
    response = client.get("/resume")
    assert response.status_code == 200
    assert b"Desole vous devez etre connecte avec ce club" in response.data


def test_resume_affiche_les_points_du_club():
    client = client_connecte("Simply Lift")
    response = client.get("/resume")
    assert response.status_code == 200
    assert b"Points disponibles : 13" in response.data


def test_pas_de_lien_de_reservation_pour_une_competition_passee():
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    client = client_connecte("Simply Lift")
    response = client.get("/resume")
    assert b"/book/Spring%20Festival/Simply%20Lift" not in response.data
    assert b"/book/Fall%20Classic/Simply%20Lift" in response.data   # à venir


def test_pas_de_lien_de_reservation_pour_une_competition_complete():
    trouver(server.competitions, "Spring Festival")['numberOfPlaces'] = "0"
    client = client_connecte("Simply Lift")
    response = client.get("/resume")
    assert b"/book/Spring%20Festival/Simply%20Lift" not in response.data


def test_lien_vers_mes_reservations_depuis_le_resume():
    client = client_connecte("Simply Lift")
    response = client.get("/resume")
    assert b'href="/mes-reservations"' in response.data
