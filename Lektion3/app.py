from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
users = {1: "Anna", 2: "Erik"}

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