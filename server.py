import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


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


def estPassee(competition):
    dateCompetition = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    return dateCompetition < datetime.now()

app.jinja_env.globals['estPassee'] = estPassee

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    matchingClubs = [club for club in clubs if club['email'] == request.form['email']]
    if not matchingClubs:
        flash("Desole ce mail existe pas")
        return render_template('index.html')
    club = matchingClubs[0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired <= 0:
        flash("Desole le nombre de places doit etre positif")
        return render_template('welcome.html', club=club, competitions=competitions)
    if estPassee(competition):
        flash("Desole cette competition est deja passee")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(club['points']):
        flash("Desole pas assez de points")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > MAX_PLACES_PAR_COMPETITION:
        flash("Desole maximum 12 places par competition")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Desole pas assez de places disponibles")
        return render_template('welcome.html', club=club, competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))