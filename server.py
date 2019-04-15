from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL

app = Flask(__name__)

app.secret_key = 'ilikecoolstuffthatisfuntodo'

def getLanguages():
   mysql = connectToMySQL("flask_survey")
   return mysql.query_db("SELECT * FROM languages;")

def getLocations():
   mysql = connectToMySQL("flask_survey")
   query = "SELECT * FROM locations;"
   return mysql.query_db(query)

def getLanguage(id):
   mysql = connectToMySQL("flask_survey")
   query = "SELECT * FROM languages WHERE id=%(id)s;"
   data = {
      "id": id
   }
   return mysql.query_db(query, data)[0]

def getLocation(id):
   mysql = connectToMySQL("flask_survey")
   query = "SELECT * FROM locations WHERE id=%(id)s;"
   data = {
      "id": id
   }
   return mysql.query_db(query, data)[0]

@app.route('/')
def index():
   data = {
      "locations": getLocations(),
      "languages": getLanguages()
   }
   return render_template("index.html", survey_data=data)

@app.route('/result', methods=['POST'])
def result():
   print('user submitted form')
   print(request.form)
   query = "INSERT INTO surveys (name, comment, fk_location, fk_language) VALUES (%(name)s, %(comment)s,%(location)s, %(language)s);"
   if(len(request.form["user_name"]) < 1):
      flash("Please enter a full name")
   if(len(request.form["comment"]) > 120):
      flash("Comment must not exceed 120 characters")
   
   values = {
      'name': request.form["user_name"],
      'location': request.form["dojo_loc"],
      'language': request.form["fav_lang"],
      'comment': request.form["comment"]
   }
   if not '_flashes' in session.keys():
      mysql = connectToMySQL("flask_survey")
      mysql.query_db(query, values)
      flash("survey successfully added to database!")
      values['language'] = getLanguage(request.form["fav_lang"])
      values['location'] = getLocation(request.form["dojo_loc"])
      return render_template("result.html", form_data=values)
   else:
      return redirect('/')

if __name__ == "__main__":
   app.run(debug=True)