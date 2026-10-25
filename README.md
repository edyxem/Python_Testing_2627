# GUDLFT – Réservation des compétitions régionales

Application Flask qui permet aux secrétaires des clubs de réserver des places dans les compétitions à venir avec les points de leur club (1 point = 1 place, 12 places maximum par club et par compétition).

Projet du cours *Méthodes de test et de validation de logiciel* (Licence 3), basé sur [Sedrickgael/Python_Testing_2627](https://github.com/Sedrickgael/Python_Testing_2627) et sur les [spécifications fonctionnelles](Spécifications+fonctionnelles.pdf).

## Fonctionnalités

- Connexion avec l'email du club et déconnexion.
- Liste des compétitions avec leur statut (*Ouverte*, *Complete*, *Terminee*), et réservation de places avec les points du club.
- Messages d'erreur : points insuffisants, plus de 12 places, compétition complète ou passée, nombre de places invalide.
- Tableau public des points des clubs, sans connexion (`/tableau-points`).
- En plus de la spécification : page *Mes reservations* et annulation d'une réservation.

## Installation

Prérequis : Python 3.10 ou plus récent.

```bash
git clone https://github.com/edyxem/Python_Testing_2627.git
cd Python_Testing_2627
python -m venv venv
venv\Scripts\Activate.ps1        # Linux / macOS : source venv/bin/activate
python -m pip install -r requirements.txt
```

## Lancer l'application

```bash
python -m flask --app server run
```

Ouvrir <http://127.0.0.1:5000> et se connecter avec un email de `clubs.json` :

| Club | Email | Points |
|---|---|---|
| Simply Lift | john@simplylift.co | 13 |
| Iron Temple | admin@irontemple.com | 4 |
| She Lifts | kate@shelifts.co.uk | 12 |

## Configuration particulière

- L'application est dans `server.py` : il faut l'indiquer à Flask avec `--app server` (ou `FLASK_APP=server.py`).
- Pas de base de données : les données viennent de `clubs.json` et `competitions.json`, lus au démarrage. Les achats et les annulations ne sont gardés qu'en mémoire : redémarrer le serveur remet les valeurs des fichiers.
- Une compétition dont la date est passée ne peut plus être réservée. Pour tester à la main, mettez des dates futures dans `competitions.json`.
- `pytest.ini` et `.coveragerc` contiennent la configuration de pytest et de coverage.

## Tests

```
tests/
├── conftest.py      remet les données à zéro avant chaque test
├── outils.py        fonctions partagées entre les tests
├── unitaires/       une seule page ou une seule fonction
├── integration/     plusieurs pages qui doivent fonctionner ensemble
├── fonctionnels/    parcours complets d'un utilisateur
└── performance/     test de charge Locust
```

```bash
python -m pytest -v                    # tous les tests
python -m pytest tests/unitaires -v    # un seul dossier
```

Avant chaque test, `conftest.py` recharge les fichiers JSON et place les compétitions en l'an 2999 : les tests ne dépendent ni les uns des autres, ni de la date du jour.

### Couverture

```bash
python -m coverage run -m pytest
python -m coverage report      # pourcentage dans le terminal
python -m coverage html        # rapport détaillé dans rapports/couverture/ (non versionné)
```

### Performance

Exigence : avec 6 utilisateurs, chargement d'une page en moins de 5 s et mise à jour des points en moins de 2 s. Lancer l'application dans un premier terminal, puis :

```bash
python -m locust -f tests/performance/locustfile.py --headless -u 6 -r 6 -t 1m --host http://127.0.0.1:5000 --html rapports/rapport_performance.html
```

Sans `--headless`, Locust ouvre une interface sur <http://localhost:8089>.

## Rapports et résultats

Les rapports sont dans `rapports/` : `rapport_tests.txt` (pytest) et `rapport_performance.html` (Locust).

| Mesure | Résultat | Objectif |
|---|---|---|
| Tests | 92 réussis (71 unitaires, 18 intégration, 3 fonctionnels) | Tous réussis |
| Couverture de `server.py` | 100 % | Au moins 60 % |
| Performance (6 utilisateurs, 1 min) | 183 requêtes, 0 échec | Aucun échec |
| Chargement le plus lent | 0,9 s | Moins de 5 s |
| Mise à jour la plus lente | 0,8 s | Moins de 2 s |

## Conventions de nommage

- **Branches** : `bug/nom-du-bug`, `fonctionnalite/nom`, `amelioration/nom`, en minuscules avec des tirets. La branche `QA` sert à la revue de code.
- **Code** : camelCase comme le code d'origine (`purchasePlaces`). Les nouveaux noms sont en français (`mesReservations`, `annulerReservation`).
- **Routes** : minuscules avec tirets (`/tableau-points`, `/mes-reservations`).
- **Textes affichés** : en français, sans accents. Les messages d'erreur commencent par « Desole ».
- **Tests** : fichiers `test_<sujet>.py` et fonctions `test_<comportement_attendu>`. Deux fichiers de test ne doivent pas porter le même nom, même dans des dossiers différents.
- **Commits** : une phrase courte en français qui dit ce que fait le commit.

## Organisation Git

- `main` ne contient que du code terminé dont tous les tests passent.
- Un bug, une fonctionnalité ou une amélioration par branche, fusionnée dans `main` par une *pull request*.
- La branche `QA` est créée depuis `main` pour la revue et n'est jamais fusionnée.

## Questions fréquentes

- **`flask run` ne trouve pas l'application** : utilisez `python -m flask --app server run`.
- **Le bouton « Reserver des places » n'apparaît pas** : la compétition est passée ou complète.
- **Mes réservations ont disparu** : le serveur a redémarré, les données ne sont gardées qu'en mémoire.

## Liens utiles

[Flask](https://flask.palletsprojects.com/) · [Jinja2](https://jinja.palletsprojects.com/) · [pytest](https://docs.pytest.org/) · [coverage](https://coverage.readthedocs.io/) · [Locust](https://docs.locust.io/)
