import server
from outils import trouver, reserver

# Les pages de connexion, de déconnexion et d'achat doivent fonctionner ensemble :
# c'est la session remplie par /showSummary qui autorise /purchasePlaces.


def connecter(client, email):
    return client.post("/showSummary", data={"email": email})


def test_achat_accepte_apres_le_login():
    client = server.app.test_client()
    connecter(client, "john@simplylift.co")
    response = reserver(client, "Simply Lift", "Spring Festival", "2", suivre_redirection=True)
    assert b"Reservation confirmee" in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 11


def test_achat_refuse_apres_le_login_d_un_autre_club():
    client = server.app.test_client()
    connecter(client, "admin@irontemple.com")
    response = reserver(client, "Simply Lift", "Spring Festival", "2", suivre_redirection=True)
    assert b"Desole vous devez etre connecte avec ce club" in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13


def test_achat_refuse_apres_deconnexion():
    client = server.app.test_client()
    connecter(client, "john@simplylift.co")
    client.get("/logout")
    response = reserver(client, "Simply Lift", "Spring Festival", "2", suivre_redirection=True)
    assert b"Desole vous devez etre connecte avec ce club" in response.data
    assert int(trouver(server.clubs, "Simply Lift")['points']) == 13
