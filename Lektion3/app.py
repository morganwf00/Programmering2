import plotly.express as px
import pandas as pd
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
users = {1: "Anna", 2: "Erik"}

df = pd.DataFrame({
    'stad': ['Stockholm','Malmö','Umeå'],
    'invånare': [980000, 360000, 130000],
    'kommun': ['Solna','n/a',]
})

@app.route("/diagram")
def diagram():
    fig = px.bar(df, x="stad", y="invånare")
    graf = fig.to_html(full_html=False)
    return render_template("diagram.html", graf=graf)

@app.route('/tabell')
def tabell():
    df = pd.DataFrame({
        'stad': ['Stockholm','Malmö','Umeå'],
        'invånare': [980000, 360000, 130000],
    })
    html = df.to_html(classes='table table-striped', index=False)
    return render_template('tabell.html', tabell=html)

@app.route('/priser')
def priser():
    priser = [
        {"tid": "10:00", "pris": 0.52},
        {"tid": "11:00", "pris": 0.61},
    ]
    return render_template("priser.html", priser=priser)

@app.route("/api/users/<int:uid>")
def get_user(uid):
    if uid not in users:
        return jsonify({"fel": "Hittades inte"}), 404
    return jsonify({"namn": users[uid]})

@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()
    users[len(users) + 1] = data["namn"]
    return jsonify(data), 201

@app.route("/")
def roten():
    return 'Ojdå ingen sökväg...', 200

@app.route("/base")
def base():
    return render_template("base.html"), 200

@app.route("/sok")
def sok():
    q = request.args.get("q", "")
    sida = request.args.get("sida", 1, type=int)
    return jsonify({"sokord": q, "sida": sida})

@app.errorhandler(404)
def inte_hittad(fel):
    return render_template("404.html"), 404

@app.errorhandler(500)
def serverfel(fel):
    return jsonify({"fel": "Något gick fel"}), 500