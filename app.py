from flask import Flask, request, render_template, jsonify, make_response
from .modules.search.search import toLean
from html import escape
from .interpreter.interpret import interpret
import requests
import json
import random

with open("./data/credentials.txt") as f:
    creds = f.read().splitlines()
ID = creds[0]
KEY = creds[1]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def Process():
    req = request.get_json()
    khl = req['khl']
    lean = toLean(khl)
    inter = interpret(lean)
    repl = inter[0]
    errors = inter[1]
    sorries=inter[2]
    res = make_response(jsonify({"lean": lean, "repl": repl, "errors": errors, "sorries": sorries}))
    return res

@app.route("/tablet")
def tablet():
    return render_template("tablet.html")

@app.route("/save-as-binary/", methods=['POST'])
def binary_saver():
    request.files['image'].save("./data/out.png")
    r = requests.post("https://api.mathpix.com/v3/text",
        files={"file": open("./data/out.png","rb")},
        data={
        "options_json": json.dumps({
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        })
        },
        headers={
            "app_id": ID,
            "app_key": KEY
        }
    )
    with open("./data/req.json", "w") as f:
        json.dump(r.json(), f)

    return jsonify({})

@app.route("/ocr",  methods=['POST'])
def read_tablet():

    with open("./data/req.json", "r") as f:
        r = json.load(f)
    with open("./data/old_req.json", "r") as f:
        rold = json.load(f)

    if r==rold:
        return make_response(jsonify({}))
    else:
        with open("./data/old_req.json", "w") as f:
            json.dump(r, f)
        res = make_response(jsonify(r))
        return res

