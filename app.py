from flask import Flask, request, render_template, jsonify, make_response
from .modules.id import toLean
from html import escape
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_entry():
    req = request.get_json()
    khl = req['name']
    lean = toLean(khl)
    res = make_response(jsonify({"message": escape(lean)}))
    return res
