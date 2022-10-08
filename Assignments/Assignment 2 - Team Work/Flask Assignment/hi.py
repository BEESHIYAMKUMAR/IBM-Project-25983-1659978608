from flask import Flask,render_template

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("/index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("/dashboard.html")


app.run(debug=True)

