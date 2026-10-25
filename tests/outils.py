import server


def client_connecte(nomClub):
    # Client de test déjà connecté avec ce club, comme après un login réussi
    client = server.app.test_client()
    with client.session_transaction() as session:
        session['club'] = nomClub
    return client
