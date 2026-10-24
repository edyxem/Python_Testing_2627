import pytest
import server


@pytest.fixture(autouse=True)
def donnees_neuves(monkeypatch):
    # Chaque test repart des données des fichiers JSON : une réservation
    # faite dans un test ne doit pas modifier les clubs ou compétitions du suivant.
    monkeypatch.setattr(server, "clubs", server.loadClubs())
    monkeypatch.setattr(server, "competitions", server.loadCompetitions())
