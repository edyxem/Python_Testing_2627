import server
from outils import trouver, client_connecte, reserver

# Plusieurs achats à la suite : la limite de 12 places porte sur le total du club

def test_cumul_de_reservations_refuse_au_dela_de_12_places():
    client = client_connecte("Simply Lift")          # 13 points
    reserver(client, "Simply Lift", "Spring Festival", "8")
    response = reserver(client, "Simply Lift", "Spring Festival", "5")    # 8 + 5 = 13 places
    assert response.status_code == 200
    assert b"Desole maximum 12 places par competition" in response.data
    # 25 - 8 : la 2e réservation n'a rien retiré
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 17

def test_cumul_de_reservations_accepte_jusqu_a_12_places():
    # Valeur limite : 8 + 4 = 12 places au total doit être accepté
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "8")
    response = reserver(client, "Simply Lift", "Spring Festival", "4", suivre_redirection=True)
    assert b"Reservation confirmee" in response.data
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 13
