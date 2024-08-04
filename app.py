from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Random Secret Key'

#MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["URL_Shortener"]
collection_url = db["All_URLs"]
collection_users = db['USERS']

#function to create random short id
def generate_short_id():
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=4))
        if not collection_url.find_one({'short_id' : short_id}):
            break
    return short_id

# Link Shortener Page Route
@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_id = generate_short_id()
        short_url = request.host_url + short_id
        collection_url.insert_one({
            'long_url' : long_url,
            'short_url' : short_url,
            'short_id' : short_id,
            'clicks' : 0,
        })

        return render_template("link-shortener.html", short_url=short_url)

    return render_template("link-shortener.html")


#Redirect route
@app.route('/<id>')
def redirect_url(id):
    x = collection_url.find_one({'short_id' : id})
    if x:
        original_link = x['long_url']
        click_increment = x['clicks'] + 1
        collection_url.update_one({'short_id' : id}, {'$set': {'clicks' : click_increment}})
        return redirect(original_link)
    else:
        flash('Invalid URL!, You did not stored this URL.')
        return redirect(url_for('home'))

#Statistics Page route
@app.route('/stats')
def stats():
    documents = collection_url.find()
    records = []
    for doc in documents:
        record = dict(doc)
        records.append(record)
    return render_template('stats.html', records=records)

#Registration Page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_mail = request.form['user_email']
        user_name = request.form['user_name']
        password = request.form['password']
        
        #checking user already exist or not
        if collection_users.find_one({'Email' : user_mail}):
            flash('User already exists!', 'Try to LogIn')
        else:
            collection_users.insert_one({
                'Email' : user_mail,
                'User Name' : user_name,
                'Password' : password,
            })
            flash('Registration Successful!', 'Welcome to the team!')
            return redirect(url_for('login'))
    return render_template('registration.html')










if __name__ == "__main__":
    app.run(debug=True)
