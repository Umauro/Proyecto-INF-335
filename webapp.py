from flask import Flask, render_template, redirect, url_for, request
import requests
import unicodedata
import json

app = Flask(__name__)

@app.route('/',methods=['get','post'])
def index():
    if request.method == 'GET':
        games = requests.get('http://localhost:5000/games')
        games = json.loads(games.text)
        return render_template('index.html', games=games)

    elif request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))
    
    


@app.route('/search/<string:query>',methods=['get','post'])
def search(query):
    if request.method == 'GET':
        result = requests.get('http://localhost:9200/games_index/_search?q=title:{}'.format(query))
        result = json.loads(result.text)
        return render_template('search.html',results=result['hits']['hits'])
    elif request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

@app.route('/game/<string:permalink>',methods=['get','post'])
def games(permalink):
    if request.method == 'GET': 
        game = requests.get('http://localhost:5000/games/{}'.format(permalink)) 
        game = json.loads(game.text)
        game_dict = json.dumps(game)
        return render_template('game.html', game=game)
    elif request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)