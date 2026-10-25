import server

# Tests des fonctions de server.py appelées directement, sans passer par une page

def test_est_passee_pour_une_date_dans_le_passe():
    assert server.estPassee({'date': "2020-03-27 10:00:00"}) is True

def test_est_passee_pour_une_date_dans_le_futur():
    assert server.estPassee({'date': "2999-03-27 10:00:00"}) is False

def test_load_clubs_lit_le_fichier_json():
    clubs = server.loadClubs()
    assert "Simply Lift" in [club['name'] for club in clubs]
    for club in clubs:
        assert set(club.keys()) == {'name', 'email', 'points'}

def test_load_competitions_lit_le_fichier_json():
    competitions = server.loadCompetitions()
    assert "Spring Festival" in [competition['name'] for competition in competitions]
    for competition in competitions:
        assert set(competition.keys()) == {'name', 'date', 'numberOfPlaces'}
