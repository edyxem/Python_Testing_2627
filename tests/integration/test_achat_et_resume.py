import server
from outils import trouver, client_connecte, reserver

# Après un achat, /purchasePlaces redirige vers /resume : on vérifie la page
# obtenue au bout de la redirection.


def test_page_apres_achat_affiche_la_confirmation_et_les_points():
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Spring Festival", "2", suivre_redirection=True)
    assert response.status_code == 200
    assert b"Reservation confirmee : 2 places achetees" in response.data
    assert b"Points disponibles : 11" in response.data


def test_message_confirmation_au_singulier_pour_une_place():
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Spring Festival", "1", suivre_redirection=True)
    assert b"Reservation confirmee : 1 place achetee" in response.data


def test_actualiser_la_page_ne_reserve_pas_une_deuxieme_fois():
    # Actualiser (F5) = refaire la dernière requête de la page affichée
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Spring Festival", "2", suivre_redirection=True)
    actualisation = client.get(response.request.path)
    assert actualisation.status_code == 200
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 11     # pas 9
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 23
