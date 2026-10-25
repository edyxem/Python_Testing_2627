import server
from outils import trouver, client_connecte

# Tests de /annuler-reservation : le club rend toutes les places réservées sur
# une compétition, récupère ses points et la compétition récupère ses places.


def preparer_reservation():
    # État après un achat de 2 places par Simply Lift sur Spring Festival
    trouver(server.clubs, "Simply Lift")['points'] = "11"
    trouver(server.competitions, "Spring Festival")['numberOfPlaces'] = "23"
    server.reservations[("Simply Lift", "Spring Festival")] = 2


def annuler(client, competition):
    return client.post("/annuler-reservation", data={"competition": competition})


def verifier_rien_n_a_change():
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 11
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 23
    assert server.reservations[("Simply Lift", "Spring Festival")] == 2


def test_annulation_rend_les_points_et_les_places():
    preparer_reservation()
    annuler(client_connecte("Simply Lift"), "Spring Festival")
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13                     # 11 + 2
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 25   # 23 + 2


def test_annulation_supprime_la_reservation():
    preparer_reservation()
    annuler(client_connecte("Simply Lift"), "Spring Festival")
    assert ("Simply Lift", "Spring Festival") not in server.reservations


def test_annulation_redirige_vers_mes_reservations():
    # Post/Redirect/Get, comme pour l'achat : actualiser ne doit pas renvoyer le formulaire
    preparer_reservation()
    response = annuler(client_connecte("Simply Lift"), "Spring Festival")
    assert response.status_code == 302
    assert response.headers['Location'] == "/mes-reservations"


def test_annulation_refusee_sans_connexion():
    preparer_reservation()
    response = annuler(server.app.test_client(), "Spring Festival")
    assert response.status_code == 200
    assert b"Desole vous devez etre connecte avec ce club" in response.data
    verifier_rien_n_a_change()


def test_annulation_refusee_sans_reservation():
    client = client_connecte("Simply Lift")
    response = annuler(client, "Fall Classic")
    assert response.status_code == 302
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13
    assert int(trouver(server.competitions, "Fall Classic")['numberOfPlaces']) == 13


def test_annulation_refusee_pour_une_competition_inconnue():
    client = client_connecte("Simply Lift")
    response = annuler(client, "Competition Inconnue")
    assert response.status_code == 302                  # pas d'erreur 500


def test_annulation_refusee_pour_la_reservation_d_un_autre_club():
    # Iron Temple n'a rien réservé : il ne peut pas annuler les places de Simply Lift
    preparer_reservation()
    annuler(client_connecte("Iron Temple"), "Spring Festival")
    verifier_rien_n_a_change()
    assert int(trouver(server.clubs, "Iron Temple")['points']) == 4


def test_annulation_refusee_pour_une_competition_passee():
    preparer_reservation()
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    annuler(client_connecte("Simply Lift"), "Spring Festival")
    verifier_rien_n_a_change()


def test_annulation_impossible_avec_get():
    # Une annulation modifie les données : elle doit passer par un formulaire (POST)
    client = client_connecte("Simply Lift")
    response = client.get("/annuler-reservation")
    assert response.status_code == 405


def test_bouton_annuler_affiche_pour_une_competition_a_venir():
    preparer_reservation()
    response = client_connecte("Simply Lift").get("/mes-reservations")
    assert b'action="/annuler-reservation"' in response.data


def test_pas_de_bouton_annuler_pour_une_competition_passee():
    preparer_reservation()
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    response = client_connecte("Simply Lift").get("/mes-reservations")
    assert b"<td>Spring Festival</td>" in response.data   # toujours listée
    assert b'action="/annuler-reservation"' not in response.data
