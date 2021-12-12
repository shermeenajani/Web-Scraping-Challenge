from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_collection = mongo.db.mars_collection
mars_data = scrape_mars.scrape()
mars_collection.replace_one({}, mars_data, upsert=True)

@app.route("/")
def index():
    mars_data = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars_parameters=mars_data)


@app.route("/scrape")
def scraper():
    mars_collection = mongo.db.mars_collection
    mars_data = scrape_mars.scrape()
    mars_collection.replace_one({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
