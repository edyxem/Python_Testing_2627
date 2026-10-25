import server
from outils import client_connecte

def test_mes_reservations_refuse_sans_connexion():
    client = server.app.test_client()
    response = client.get("/mes-reservations")
    assert response.status_code == 200
    assert b"Desole vous devez etre connecte avec ce club" in response.data

def test_mes_reservations_vide_au_depart():
    client = client_connecte("Simply Lift")
    response = client.get("/mes-reservations")
    assert response.status_code == 200
    assert b"Aucune reservation pour le moment" in response.data

def test_mes_reservations_affiche_les_reservations_du_club():
    # On remplit directement le dictionnaire, sans passer par un achat
    server.reservations[("Simply Lift", "Spring Festival")] = 2
    client = client_connecte("Simply Lift")
    response = client.get("/mes-reservations")
    assert b"<td>Spring Festival</td>" in response.data
    assert b"<td>2</td>" in response.data
    assert b"Aucune reservation pour le moment" not in response.data

def test_mes_reservations_n_affiche_pas_celles_des_autres_clubs():
    server.reservations[("Iron Temple", "Fall Classic")] = 1
    client = client_connecte("Simply Lift")
    response = client.get("/mes-reservations")
    assert b"Fall Classic" not in response.data
    assert b"Aucune reservation pour le moment" in response.data
