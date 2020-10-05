from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
# Create an instance of Flask
app = Flask(__name__)
# set up mongo connection Or set inline
mongo = PyMongo(app, uri ="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    # return "web scrape was succcefully completed"
    return redirect(url_for('index'), code=302)

if __name__ == "__main__":
    app.run(debug=True)