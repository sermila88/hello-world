from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name1 = request.form.get("name1")
    input_name2 = request.form.get("name2")

    input_age1 = request.form.get("age1")
    input_age2 = request.form.get("age2")
    return render_template(
        "hello.html",
        name1=input_name1,
        name2=input_name2,
        age1=input_age1,
        age2=input_age2,
    )


def process_query(query):
    if query.lower() == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    else:
        return "Unknown"


@app.route("/query")
def query():
    query = request.args.get("q")
    result = process_query(query)
    return render_template(
        "query.html",
        query=query,
        result=result,
    )
