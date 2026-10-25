import server
from outils import client_connecte, reserver

# Un achat doit se voir tout de suite sur le tableau des points et sur "Mes reservations"


def test_tableau_a_jour_apres_une_reservation():
    client = client_connecte("Simply Lift")         # 13 points
    reserver(client, "Simply Lift", "Spring Festival", "2")
    response = server.app.test_client().get("/tableau-points")   # visiteur non connecté
    assert b"<td>11</td>" in response.data
    assert b"<td>13</td>" not in response.data


def test_mes_reservations_affiche_l_achat():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    response = client.get("/mes-reservations")
    assert b"<td>Spring Festival</td>" in response.data
    assert b"<td>2</td>" in response.data


def test_mes_reservations_additionne_les_achats_successifs():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    reserver(client, "Simply Lift", "Spring Festival", "3")
    response = client.get("/mes-reservations")
    assert b"<td>5</td>" in response.data            # 2 + 3, sur une seule ligne


def test_mes_reservations_ignore_les_achats_d_un_autre_club():
    autreClub = client_connecte("Iron Temple")
    reserver(autreClub, "Iron Temple", "Fall Classic", "1")
    client = client_connecte("Simply Lift")
    response = client.get("/mes-reservations")
    assert b"Fall Classic" not in response.data
