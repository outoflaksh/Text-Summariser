from flask import Flask, json, render_template,  request, jsonify
from text_summ2 import summarise

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods = ['POST', 'GET'])
def summary():
    url = request.form.get("url")
    try:
        summary = summarise(url)
    except:
        return render_template("index.html", summary = "Sorry, summary could not be created!")
    return render_template("index.html", summary = summary)

@app.route("/summarise", methods = ['POST'])
def get_summary():
    data = request.get_json()
    #validate url
    try:
        summary = summarise(data['url'])
    except:
        return jsonify({'message' : 'Summary could not be created!'})

    return jsonify({'summary' : summary})

if __name__ == "__main__":
    app.run(debug=True)
