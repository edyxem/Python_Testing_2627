import server


def trouver(liste, nom):
    # Club ou compétition qui porte ce nom
    return [element for element in liste if element['name'] == nom][0]


def client_connecte(nomClub):
    # Client de test déjà connecté avec ce club, comme après un login réussi
    client = server.app.test_client()
    with client.session_transaction() as session:
        session['club'] = nomClub
    return client


def reserver(client, club, competition, places, suivre_redirection=False):
    # Envoie le formulaire d'achat de places, comme le bouton "Reserver"
    return client.post("/purchasePlaces", data={
        "club": club,
        "competition": competition,
        "places": places,
    }, follow_redirects=suivre_redirection)
