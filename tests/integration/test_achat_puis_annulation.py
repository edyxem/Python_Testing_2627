import server
from outils import trouver, client_connecte, reserver

# Une annulation après un vrai achat : les pages d'achat, d'annulation,
# "Mes reservations" et le tableau des points doivent rester d'accord entre elles.

def annuler(client, competition):
    return client.post("/annuler-reservation", data={"competition": competition},
                       follow_redirects=True)

def test_achat_puis_annulation_remet_tout_comme_avant():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    response = annuler(client, "Spring Festival")
    assert b"Reservation annulee : 2 places rendues" in response.data
    assert b"Aucune reservation pour le moment" in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13
    assert int(trouver(server.competitions, "Spring Festival")['numberOfPlaces']) == 25

def test_message_annulation_au_singulier_pour_une_place():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "1")
    response = annuler(client, "Spring Festival")
    assert b"Reservation annulee : 1 place rendue" in response.data

def test_message_d_erreur_si_rien_a_annuler():
    client = client_connecte("Simply Lift")
    response = annuler(client, "Spring Festival")
    assert b"Desole aucune reservation a annuler pour cette competition" in response.data

def test_message_d_erreur_pour_une_competition_passee():
    client = client_connecte("Simply Lift")
    reserver(client, "Simply Lift", "Spring Festival", "2")
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    response = annuler(client, "Spring Festival")
    assert b"Desole cette competition est deja passee" in response.data

def test_apres_annulation_on_peut_de_nouveau_reserver_12_places():
    # Les places annulées ne comptent plus dans la limite de 12 par club
    client = client_connecte("Simply Lift")              # 13 points
    reserver(client, "Simply Lift", "Spring Festival", "8")
    annuler(client, "Spring Festival")
    response = reserver(client, "Simply Lift", "Spring Festival", "12", suivre_redirection=True)
    assert b"Reservation confirmee : 12 places achetees" in response.data

def test_tableau_des_points_a_jour_apres_annulation():
    client = client_connecte("Iron Temple")               # 4 points
    reserver(client, "Iron Temple", "Spring Festival", "3")
    annuler(client, "Spring Festival")
    tableau = server.app.test_client().get("/tableau-points")
    assert b"<td>4</td>" in tableau.data
    assert b"<td>1</td>" not in tableau.data
