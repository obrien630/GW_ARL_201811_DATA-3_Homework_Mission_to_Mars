from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/db"

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

# Route to render index.html template and find mongo documents
@app.route("/")
def index():

    mars_data = mongo.db.collection.find()
      
    print(mars_data) 
    
    # return template and data
    return render_template("index.html", mars_data=mars_data)  

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Scrape functions
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
   
    news_title = mars_data["news_data"]["news_title"]
    news_paragraph = mars_data["news_data"],["paragraph_text"]
    featured_image_url = mars_data["mars_featured_image"]
    mars_weather = mars_data["mars_weather"]
    mars_facts_table = mars_data["mars_facts_table"]
    hemisphere_title1 = mars_data["mars_hemispheres"][0]["title"]
    hemisphere_img1 = mars_data["mars_hemispheres"][0]["hem_url"]
    hemisphere_title2 = mars_data["mars_hemispheres"][1]["title"]
    hemisphere_img2 = mars_data["mars_hemispheres"][1]["hem_url"]
    hemisphere_title3 = mars_data["mars_hemispheres"][2]["title"]
    hemisphere_img3 = mars_data["mars_hemispheres"][2]["hem_url"]
    hemisphere_title4 = mars_data["mars_hemispheres"][3]["title"]
    hemisphere_img4 = mars_data["mars_hemispheres"][3]["hem_url"]
    
    mongo.db.collection.insert(mars_data)
   
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)