import server


def pytest_runtest_setup(item):
    # pytest appelle cette fonction avant chaque test : chaque test repart des
    # données des fichiers JSON, une réservation faite dans un test ne doit pas
    # modifier les clubs ou compétitions du suivant.
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    server.reservations = {}
    # Les compétitions sont mises en l'an 2999 pour que les tests ne cassent pas
    # quand les dates du fichier seront passées. Un test qui a besoin d'une
    # compétition passée change sa date lui-même.
    for competition in server.competitions:
        competition['date'] = "2999" + competition['date'][4:]
