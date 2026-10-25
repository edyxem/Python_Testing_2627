import server
from outils import client_connecte

def connecter(email):
    client = server.app.test_client()
    return client.post("/showSummary", data={"email": email})

def test_login_avec_email_valide():
    response = connecter("john@simplylift.co")
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

def test_login_avec_email_inconnu():
    response = connecter("inconnu@test.com")
    assert response.status_code == 200
    assert b"Desole ce mail existe pas" in response.data   # le message d'erreur attendu

def test_login_avec_email_en_majuscules():
    response = connecter("JOHN@SimplyLift.co")
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

def test_login_avec_espaces_autour_de_l_email():
    # Cas fréquent : un espace copié-collé avec l'email
    response = connecter("  john@simplylift.co ")
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

def test_login_toujours_refuse_pour_un_email_inconnu():
    # Non-régression : la tolérance ne doit pas accepter n'importe quoi
    response = connecter("  INCONNU@test.com ")
    assert b"Desole ce mail existe pas" in response.data

def test_logout_vide_la_session_et_revient_a_l_accueil():
    client = client_connecte("Simply Lift")
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers['Location'] == "/"
    with client.session_transaction() as session:
        assert 'club' not in session
