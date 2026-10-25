from locust import HttpUser, task, between

# Test de performance demandé par la spécification (guide de développement, point 5) :
# avec 6 utilisateurs, une page ne doit jamais mettre plus de 5 secondes à charger,
# et une mise à jour des points pas plus de 2 secondes.
# Une requête trop lente est comptée en échec dans le rapport de Locust.

TEMPS_MAX_CHARGEMENT = 5
TEMPS_MAX_MISE_A_JOUR = 2

CLUBS = [
    ("Simply Lift", "john@simplylift.co"),
    ("Iron Temple", "admin@irontemple.com"),
    ("She Lifts", "kate@shelifts.co.uk"),
]


class Secretaire(HttpUser):
    wait_time = between(1, 3)
    nombreDeSecretaires = 0

    def on_start(self):
        # Chaque utilisateur se connecte avec un club, à tour de rôle
        self.nomClub, email = CLUBS[Secretaire.nombreDeSecretaires % len(CLUBS)]
        Secretaire.nombreDeSecretaires += 1
        self.client.post("/showSummary", data={"email": email})

    def verifier(self, response, tempsMax, attendu):
        temps = response.elapsed.total_seconds()
        if attendu(response):
            if temps > tempsMax:
                response.failure("Trop lent : " + str(temps) + " s (maximum " + str(tempsMax) + " s)")
            else:
                response.success()
        else:
            response.failure("Reponse inattendue (code " + str(response.status_code) + ")")

    @task(3)
    def liste_des_competitions(self):
        with self.client.get("/resume", catch_response=True) as response:
            self.verifier(response, TEMPS_MAX_CHARGEMENT, lambda r: b"Competitions:" in r.content)

    @task(2)
    def tableau_des_points(self):
        with self.client.get("/tableau-points", catch_response=True) as response:
            self.verifier(response, TEMPS_MAX_CHARGEMENT, lambda r: b"Points des clubs" in r.content)

    @task(1)
    def reserver_puis_annuler(self):
        # La réservation met à jour les points du club. On l'annule juste après pour
        # rendre les points : le test peut tourner longtemps sans vider les clubs.
        with self.client.post("/purchasePlaces", data={
            "club": self.nomClub,
            "competition": "Fall Classic",
            "places": "1",
        }, allow_redirects=False, catch_response=True, name="/purchasePlaces (mise a jour)") as response:
            self.verifier(response, TEMPS_MAX_MISE_A_JOUR, lambda r: r.status_code == 302)
        with self.client.post("/annuler-reservation", data={"competition": "Fall Classic"},
                              allow_redirects=False, catch_response=True,
                              name="/annuler-reservation (mise a jour)") as response:
            self.verifier(response, TEMPS_MAX_MISE_A_JOUR, lambda r: r.status_code == 302)
