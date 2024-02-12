from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)     

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

def get_commit_data(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        commits = response.json()
        commit_dates = [commit['commit']['author']['date'] for commit in commits]
        commit_dates = [datetime.fromisoformat(date[:-1]) for date in commit_dates]
        commit_counts = {}
        for date in commit_dates:
            minute = date.replace(second=0, microsecond=0)
            commit_counts[minute] = commit_counts.get(minute, 0) + 1
        return commit_counts
    else:
        print(f"Erreur lors de la récupération des commits : {response.status_code}")
        return None

@app.route('/commits/')
def plot_commit_graph():
    repo_owner = "OpenRSI"
    repo_name = "5MCSI_Metriques"

    commit_data = get_commit_data(repo_owner, repo_name)
    if commit_data:
        minutes = list(commit_data.keys())
        commit_count = list(commit_data.values())
        
        return render_template('commit_graph.html', minutes=minutes, commit_count=commit_count)
    else:
        return "Erreur lors de la récupération des données des commits."

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
  
if __name__ == "__main__":
  app.run(debug=True)
