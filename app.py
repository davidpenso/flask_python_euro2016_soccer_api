from flask import Flask, render_template, request, redirect
import requests
app = Flask(__name__)

api_key='a39b4c6be2144387b5db50d701bf8e42'
base='https://api.crowdscores.com/api/v1/'
headers = {
                 'x-crowdscores-api-key': api_key,
                 'Content-Type': 'application/json'
                }

class Teams():
	def __init__(self, compid):
		self.teams=[]
		self.flags=[]
		self.cid=compid
	def get_teams_name(self):
		endpoint='teams?competition_id='+self.cid
		r = requests.get(base + endpoint, headers=headers)
		teams= r.json()
		self.teams=[i['name'] for i in teams if i['showLeagueTables']]
		return self.teams
	def get_flag(self):
		endpoint='teams?competition_id='+self.cid
		r = requests.get(base + endpoint, headers=headers)
		teams= r.json()
		self.flags=[i['flagUrl'] for i in teams if i['showLeagueTables']]
		return self.flags

class Matches():
	def __init__(self, compid):
		self.home=[]
		self.away=[]
		self.venue=[]
		self.cid=compid
	def get_hometeam_name(self):
		endpoint='matches?competition_id='+self.cid
		r = requests.get(base + endpoint, headers=headers)
		h= r.json()
		self.home=[i['homeTeam']['name'] for i in h]
		return self.home
	def get_awayteam_name(self):
		endpoint='matches?competition_id='+self.cid
		r = requests.get(base + endpoint, headers=headers)
		a= r.json()
		self.away=[i['awayTeam']['name'] for i in a]
		return self.away
	def get_venue_name(self):
		endpoint='matches?competition_id='+self.cid
		r = requests.get(base + endpoint, headers=headers)
		v= r.json()
		self.venue=[i['venue']['name'] for i in v]
		return self.venue

class Tournament(Teams, Matches):
	def __init__(self, compid):
		self.cid=compid
		self.teams=self.get_teams_name()
		self.home=self.get_hometeam_name()
		self.away=self.get_awayteam_name()
		self.flag=self.get_flag()
		self.groups=[]
	def get_groups(self):
		endpoint='league-tables?competition_id='+self.cid
		r = requests.get(base + endpoint, headers=headers)
		v= r.json()
		self.venue=[i['venue']['name'] for i in v]
		return self.venue


europa=Tournament('267')

l=[]
for team, flag in zip(europa.teams,europa.flag):
	l.append({'t':team, 'f':flag})
ma=[]
for home, away in zip(europa.home,europa.away):
	ma.append({'home':home, 'away':away})

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/teams')
def team():
	return render_template('teams.html', t=l)
@app.route('/matches')
def match():
	return render_template('matches.html', m=ma)

app.run()