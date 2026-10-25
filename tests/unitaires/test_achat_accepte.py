import server
from outils import trouver, client_connecte, reserver

# Tests de /purchasePlaces quand l'achat doit être accepté


def test_achat_reussi_redirige_vers_une_page_en_get():
    # Post/Redirect/Get : après un achat, le serveur redirige au lieu d'afficher la page
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Spring Festival", "2")
    assert response.status_code == 302
    assert response.headers['Location'] == "/resume"


def test_achat_deduit_les_points_et_les_places():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 11                   # 13 - 2
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 23   # 25 - 2


def test_achat_enregistre_la_reservation_du_club():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    assert server.reservations == {("Simply Lift", "Spring Festival"): 2}


def test_achat_accepte_avec_exactement_12_places():
    # Valeur limite : 12 places doit rester autorisé
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "12")
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 13   # 25 - 12


def test_achat_accepte_avec_les_dernieres_places():
    # Valeur limite : réserver exactement les places restantes doit fonctionner
    trouver(server.competitions, "Fall Classic")['numberOfPlaces'] = "2"
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Fall Classic", "2")
    assert int(trouver(server.competitions, "Fall Classic")['numberOfPlaces']) == 0


def test_achat_accepte_avec_tous_les_points_du_club():
    # Valeur limite : Iron Temple dépense ses 4 points
    client = client_connecte("Iron Temple")
    reserver(client, "Iron Temple", "Spring Festival", "4")
    assert int(trouver(server.clubs, "Iron Temple")['points']) == 0
