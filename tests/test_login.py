import server

def test_login_avec_email_valide():
    client = server.app.test_client()
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200

def test_login_avec_email_inconnu():
    client = server.app.test_client()
    response = client.post("/showSummary", data={"email": "inconnu@test.com"})
    assert response.status_code == 200
    assert b"Desole ce mail existe pas" in response.data   # le message d'erreur attendu
