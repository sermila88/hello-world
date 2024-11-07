from flask import Flask, render_template, request
import re
from sympy import isprime
import requests

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


def product(ints):
    result = 1
    for i in ints:
        result *= i
    return result


def process_query(query):
    if query.lower() == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if "your name" in query.lower():
        return "Sermila and Rob"
    if "plus" in query.lower():
        return str(sum([int(s) for s in re.findall(r"\d+", query)]))
    if "multiplied" in query.lower():
        return str(product([int(s) for s in re.findall(r"\d+", query)]))
    if "minus" in query.lower():
        numbers = [int(s) for s in re.findall(r"\d+", query)]
        minus = numbers[0] - numbers[1]
        return str(minus)
    if "power" in query.lower():
        numbers = [int(s) for s in re.findall(r"\d+", query)]
        result = pow(numbers[0], numbers[1])
        return str(result)
    if "prime" in query.lower():
        numbers = [int(s) for s in re.findall(r"\d+", query)]
        prime_nums = [int(number) for number in numbers if isprime(number)]
        return str(prime_nums)
    else:
        return "Unknown"


@app.route("/query")
def query():
    query = request.args.get("q")
    result = process_query(query)
    return result


@app.route("/username")
def username():
    return render_template("username.html")


@app.route("/username/submit", methods=["POST"])
def submit_username():
    input_username = request.form.get("name")
    url = "https://api.github.com/users/" + input_username + "/repos"
    data = []
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            commit_data = []
            languages_data = []
            fullname = repo["full_name"]
            url_stem = "https://api.github.com/repos/"
            languages_url = url_stem + fullname + "/languages"
            languages_response = requests.get(languages_url)
            if languages_response.status_code == 200:
                languages_response = languages_response.json()
                for language in languages_response:
                    languages_data.append(language)
            else:
                return "Error fetching languages"
            commit_url = url_stem + fullname + "/commits"
            commit_response = requests.get(commit_url)
            if commit_response.status_code == 200:
                commits = commit_response.json()
                for commit in commits:
                    commit_hash = commit["sha"]
                    author = commit["commit"]["committer"]["name"]
                    date = commit["commit"]["committer"]["date"]
                    message = commit["commit"]["message"]
                    commit_data.append(
                        {
                            "commit_hash": commit_hash,
                            "author": author,
                            "date": date,
                            "message": message,
                        }
                    )
            else:
                return "Error fetching the commit data from the API"
            data.append(
                {
                    "fullname": fullname,
                    "commits": commit_data,
                    "languages": languages_data,
                }
            )
        return render_template("repos.html", data=data)
    else:
        return "Error fetching the repo data from the API"
