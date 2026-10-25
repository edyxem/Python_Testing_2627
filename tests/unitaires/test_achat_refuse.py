import server
from outils import trouver, client_connecte, reserver

# Tests de /purchasePlaces quand l'achat doit être refusé :
# le message d'erreur s'affiche et ni les points ni les places ne changent.

def verifier_rien_n_a_change(club, points, competition, places):
    assert int(trouver(server.clubs, club)['points']) == points
    assert int(trouver(server.competitions, competition)['numberOfPlaces']) == places

def test_achat_avec_competition_inconnue():
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Competition Inconnue", "1")
    assert response.status_code == 200
    assert b"Desole club ou competition introuvable" in response.data

def test_achat_avec_club_inconnu():
    client = client_connecte("Simply Lift")
    response = reserver(client, "Club Inconnu", "Spring Festival", "1")
    assert response.status_code == 200
    assert b"Desole club ou competition introuvable" in response.data

def test_achat_refuse_sans_connexion():
    client = server.app.test_client()
    response = reserver(client, "Simply Lift", "Spring Festival", "2")
    assert response.status_code == 200
    assert b"Desole vous devez etre connecte avec ce club" in response.data
    verifier_rien_n_a_change("Simply Lift", 13, "Spring Festival", 25)

def test_achat_refuse_pour_un_autre_club():
    # Connecté en tant que Iron Temple, on essaie de dépenser les points de Simply Lift
    client = client_connecte("Iron Temple")
    response = reserver(client, "Simply Lift", "Spring Festival", "2")
    assert b"Desole vous devez etre connecte avec ce club" in response.data
    verifier_rien_n_a_change("Simply Lift", 13, "Spring Festival", 25)

def test_achat_refuse_avec_un_champ_vide():
    # Cas réel : le secrétaire clique sur Reserver sans rien saisir
    client = client_connecte("Iron Temple")
    response = reserver(client, "Iron Temple", "Spring Festival", "")
    assert response.status_code == 200          # pas d'erreur 500
    assert b"Desole veuillez entrer un nombre de places valide" in response.data

def test_achat_refuse_avec_du_texte():
    client = client_connecte("Iron Temple")
    response = reserver(client, "Iron Temple", "Spring Festival", "abc")
    assert response.status_code == 200
    assert b"Desole veuillez entrer un nombre de places valide" in response.data
    verifier_rien_n_a_change("Iron Temple", 4, "Spring Festival", 25)

def test_achat_refuse_avec_un_nombre_de_places_negatif():
    client = client_connecte("Iron Temple")
    response = reserver(client, "Iron Temple", "Spring Festival", "-5")
    assert response.status_code == 200
    assert b"Desole le nombre de places doit etre positif" in response.data
    verifier_rien_n_a_change("Iron Temple", 4, "Spring Festival", 25)   # pas de points gagnés

def test_achat_refuse_avec_zero_place():
    client = client_connecte("Iron Temple")
    response = reserver(client, "Iron Temple", "Spring Festival", "0")
    assert response.status_code == 200
    assert b"Desole le nombre de places doit etre positif" in response.data

def test_achat_refuse_pour_une_competition_passee():
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Spring Festival", "1")
    assert response.status_code == 200
    assert b"Desole cette competition est deja passee" in response.data
    verifier_rien_n_a_change("Simply Lift", 13, "Spring Festival", 25)

def test_achat_refuse_si_points_insuffisants():
    client = client_connecte("Iron Temple")
    response = reserver(client, "Iron Temple", "Spring Festival", "5")     # 4 points seulement
    assert response.status_code == 200
    assert b"Desole pas assez de points" in response.data
    verifier_rien_n_a_change("Iron Temple", 4, "Spring Festival", 25)

def test_achat_refuse_si_plus_de_12_places():
    client = client_connecte("Simply Lift")
    # Assez de points (13) et de places (25), mais plus de 12
    response = reserver(client, "Simply Lift", "Spring Festival", "13")
    assert response.status_code == 200
    assert b"Desole maximum 12 places par competition" in response.data
    verifier_rien_n_a_change("Simply Lift", 13, "Spring Festival", 25)

def test_achat_refuse_si_pas_assez_de_places():
    trouver(server.competitions, "Fall Classic")['numberOfPlaces'] = "2"   # presque complète
    client = client_connecte("Simply Lift")
    response = reserver(client, "Simply Lift", "Fall Classic", "3")
    assert response.status_code == 200
    assert b"Desole pas assez de places disponibles" in response.data
    verifier_rien_n_a_change("Simply Lift", 13, "Fall Classic", 2)
