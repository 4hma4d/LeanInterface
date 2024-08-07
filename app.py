from flask import Flask, request, render_template, jsonify, make_response
from .modules.search.search import toLean
from html import escape
from .interpreter.interpret import interpret
import requests
import json

creds = open("credentials.txt").read().splitlines()
ID = creds[0]
KEY = creds[1]
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_entry():
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
    request.files['image'].save("out.png")
    return jsonify({})

@app.route("/ocr",  methods=['POST'])
def read_tablet():
    #Save file
    
    #Make Request
    r = requests.post("https://api.mathpix.com/v3/text",
        files={"file": open("out.png","rb")},
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
    res = make_response(jsonify(r.json()))
    return res
