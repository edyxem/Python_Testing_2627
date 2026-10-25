import server
from outils import client_connecte

def trouver(liste, nom):
    return [element for element in liste if element['name'] == nom][0]

def reserver(client, club, competition, places):
    trouver(server.competitions, competition)['date'] = "2999-03-27 10:00:00"
    return client.post("/purchasePlaces", data={
        "club": club,
        "competition": competition,
        "places": places,
    })

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

def test_mes_reservations_affiche_la_competition_et_les_places():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    response = client.get("/mes-reservations")
    assert b"<td>Spring Festival</td>" in response.data
    assert b"<td>2</td>" in response.data
    assert b"Aucune reservation pour le moment" not in response.data

def test_mes_reservations_additionne_les_reservations_successives():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    reserver(client, "Simply Lift", "Spring Festival", "3")
    response = client.get("/mes-reservations")
    assert b"<td>5</td>" in response.data            # 2 + 3, sur une seule ligne

def test_mes_reservations_n_affiche_pas_celles_des_autres_clubs():
    autreClub = client_connecte("Iron Temple")
    reserver(autreClub, "Iron Temple", "Fall Classic", "1")
    client = client_connecte("Simply Lift")
    response = client.get("/mes-reservations")
    assert b"Fall Classic" not in response.data
    assert b"Aucune reservation pour le moment" in response.data

def test_lien_vers_mes_reservations_depuis_le_resume():
    client = client_connecte("Simply Lift")
    response = client.get("/resume")
    assert b'href="/mes-reservations"' in response.data
