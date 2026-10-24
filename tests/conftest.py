import server


def pytest_runtest_setup(item):
    # pytest appelle cette fonction avant chaque test : chaque test repart des
    # données des fichiers JSON, une réservation faite dans un test ne doit pas
    # modifier les clubs ou compétitions du suivant.
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
