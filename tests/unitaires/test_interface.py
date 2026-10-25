import server
from outils import trouver, client_connecte

# Tests de l'interface : feuille de style commune, menu de navigation,
# formulaires accessibles et statut des compétitions.

FEUILLE_DE_STYLE = b'href="/static/style.css"'


def test_feuille_de_style_servie():
    client = server.app.test_client()
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert response.mimetype == "text/css"


def test_feuille_de_style_sur_les_pages_publiques():
    client = server.app.test_client()
    for page in ["/", "/tableau-points"]:
        assert FEUILLE_DE_STYLE in client.get(page).data, page


def test_feuille_de_style_sur_les_pages_du_club():
    client = client_connecte("Simply Lift")
    for page in ["/resume", "/mes-reservations", "/book/Spring Festival/Simply Lift"]:
        assert FEUILLE_DE_STYLE in client.get(page).data, page


def test_menu_d_un_visiteur_sans_deconnexion():
    response = server.app.test_client().get("/tableau-points")
    assert b'<nav' in response.data
    assert b'href="/"' in response.data                # retour à l'accueil
    assert b'href="/logout"' not in response.data      # personne à déconnecter


def test_menu_d_un_club_connecte():
    response = client_connecte("Simply Lift").get("/tableau-points")
    assert b'href="/resume"' in response.data
    assert b'href="/mes-reservations"' in response.data
    assert b'href="/logout"' in response.data


def test_champ_email_relie_a_son_etiquette():
    # Cliquer sur "Email:" doit placer le curseur dans le champ (accessibilité)
    response = server.app.test_client().get("/")
    assert b'for="email"' in response.data
    assert b'id="email"' in response.data


def test_champ_places_relie_a_son_etiquette_et_obligatoire():
    response = client_connecte("Simply Lift").get("/book/Spring Festival/Simply Lift")
    assert b'for="places"' in response.data
    assert b'id="places"' in response.data
    assert b'required' in response.data
    assert b'min="1"' in response.data


def test_maximum_du_champ_places_limite_a_12():
    # Simply Lift : 13 points, 25 places libres -> c'est la limite de 12 qui compte
    response = client_connecte("Simply Lift").get("/book/Spring Festival/Simply Lift")
    assert b'max="12"' in response.data


def test_maximum_du_champ_places_limite_aux_points_du_club():
    # Iron Temple : 4 points seulement
    response = client_connecte("Iron Temple").get("/book/Spring Festival/Iron Temple")
    assert b'max="4"' in response.data


def test_maximum_du_champ_places_limite_aux_places_restantes():
    trouver(server.competitions, "Spring Festival")['numberOfPlaces'] = "3"
    response = client_connecte("Simply Lift").get("/book/Spring Festival/Simply Lift")
    assert b'max="3"' in response.data


def test_maximum_du_champ_places_tient_compte_des_reservations_deja_faites():
    server.reservations[("Simply Lift", "Spring Festival")] = 8      # il reste 12 - 8 = 4
    response = client_connecte("Simply Lift").get("/book/Spring Festival/Simply Lift")
    assert b'max="4"' in response.data


def test_statut_des_competitions_sur_le_resume():
    trouver(server.competitions, "Spring Festival")['date'] = "2020-03-27 10:00:00"
    trouver(server.competitions, "Fall Classic")['numberOfPlaces'] = "0"
    response = client_connecte("Simply Lift").get("/resume")
    assert b"Terminee" in response.data       # Spring Festival est passée
    assert b"Complete" in response.data       # Fall Classic n'a plus de places


def test_statut_ouverte_pour_une_competition_disponible():
    response = client_connecte("Simply Lift").get("/resume")
    assert b"Ouverte" in response.data
    assert b"Terminee" not in response.data
