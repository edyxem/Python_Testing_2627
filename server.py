import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for,session


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

MAX_PLACES_PAR_COMPETITION = 12

competitions = loadCompetitions()
clubs = loadClubs()
# Places déjà réservées par chaque club sur chaque compétition : {(club, competition): places}
reservations = {}


def estPassee(competition):
    dateCompetition = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    return dateCompetition < datetime.now()

app.jinja_env.globals['estPassee'] = estPassee

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    emailSaisi = request.form['email'].strip().lower()
    matchingClubs = [club for club in clubs if club['email'].lower() == emailSaisi]
    if not matchingClubs:
        flash("Desole ce mail existe pas")
        return render_template('index.html')
    club = matchingClubs[0]
    session['club'] = club['name']
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    matchingClubs = [c for c in clubs if c['name'] == club]
    matchingCompetitions = [c for c in competitions if c['name'] == competition]
    if not matchingClubs or not matchingCompetitions:
        flash("Desole club ou competition introuvable")
        return render_template('index.html')
    if session.get('club') != club:
        flash("Desole vous devez etre connecte avec ce club")
        return render_template('index.html')
    foundClub = matchingClubs[0]
    foundCompetition = matchingCompetitions[0]
    if estPassee(foundCompetition):
        flash("Desole cette competition est deja passee")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    if int(foundCompetition['numberOfPlaces']) <= 0:
        flash("Desole cette competition est complete")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    return render_template('booking.html',club=foundClub,competition=foundCompetition)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    matchingCompetitions = [c for c in competitions if c['name'] == request.form['competition']]
    matchingClubs = [c for c in clubs if c['name'] == request.form['club']]
    if not matchingClubs or not matchingCompetitions:
        flash("Desole club ou competition introuvable")
        return render_template('index.html')
    competition = matchingCompetitions[0]
    club = matchingClubs[0]
    if session.get('club') != club['name']:
        flash("Desole vous devez etre connecte avec ce club")
        return render_template('index.html')
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        flash("Desole veuillez entrer un nombre de places valide")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired <= 0:
        flash("Desole le nombre de places doit etre positif")
        return render_template('welcome.html', club=club, competitions=competitions)
    if estPassee(competition):
        flash("Desole cette competition est deja passee")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(club['points']):
        flash("Desole pas assez de points")
        return render_template('welcome.html', club=club, competitions=competitions)
    cleReservation = (club['name'], competition['name'])
    placesDejaReservees = reservations.get(cleReservation, 0)
    if placesDejaReservees + placesRequired > MAX_PLACES_PAR_COMPETITION:
        flash("Desole maximum 12 places par competition")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Desole pas assez de places disponibles")
        return render_template('welcome.html', club=club, competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    reservations[cleReservation] = placesDejaReservees + placesRequired
    if placesRequired == 1:
        flash("Reservation confirmee : 1 place achetee")
    else:
        flash("Reservation confirmee : " + str(placesRequired) + " places achetees")
    return redirect(url_for('resume'))


def resume():
    matchingClubs = [c for c in clubs if c['name'] == session.get('club')]
    if not matchingClubs:
        flash("Desole vous devez etre connecte avec ce club")
        return render_template('index.html')
    return render_template('welcome.html', club=matchingClubs[0], competitions=competitions)

app.add_url_rule('/resume', view_func=resume)


def tableauPoints():
    return render_template('tableau_points.html', clubs=clubs)

app.add_url_rule('/tableau-points', view_func=tableauPoints)


@app.route('/logout')
def logout():
    session.pop('club', None)
    return redirect(url_for('index'))