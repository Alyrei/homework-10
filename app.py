from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Set route
@app.route('/')
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Set /scrape
@app.route("/scrape")
def scrape():
    mars = client.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)