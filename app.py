from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mar= mongo.db.collection.find_one()
    print(mar)
    return render_template("index.html", mars=mar)

@app.route("/scrape")
def web_scrape():
    mars_info = scrape()
    mongo.db.collection.update({}, mars_info, upsert=True)
    return redirect("/",code=302)    

if __name__ == "__main__":
    app.run(debug=True)



