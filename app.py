from flask import Flask, request, render_template, jsonify, make_response
from .modules.search.search import toLean
from html import escape
from .interpreter.interpret import interpret
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_entry():
    req = request.get_json()
    khl = req['name']
    lean = toLean(khl)
    inter = interpret(lean)
    repl = inter[0]
    errors = inter[1]
    sorries=inter[2]
    res = make_response(jsonify({"lean": escape(lean), "repl": repl, "errors": errors, "sorries": sorries}))
    return res

@app.route("/tablet")
def tablet():
    return render_template("tablet.html")
