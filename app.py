from flask import Flask, render_template, request, redirect, url_for
import pymongo
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Random Secret Key'

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["URL_Shortener"]
collection = db["All_URLs"]

def generate_short_id():
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=4))
        if not collection.find_one({'short_id' : short_id}):
            break
    return short_id


@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_id = generate_short_id()
        short_url = request.host_url + short_id
        collection.insert_one({
            'long_url' : long_url,
            'short_url' : short_url,
            'short_id' : short_id,
            'clicks' : 0,
        })

        return render_template("base.html", short_url=short_url)

    return render_template("base.html")

@app.route('/<id>')
def redirect_url(id):
    x = collection.find_one({'short_id' : id})
    if x:
        original_link = x['long_url']
        click_increment = x['clicks'] + 1
        collection.update_one({'short_id' : id}, {'$set': {'clicks' : click_increment}})
        return redirect(original_link)
    else:
        flash('Invalid URL!, You did not stored this URL.')
        return redirect(url_for('home'))

@app.route('/stats')
def stats():
    documents = collection.find()
    records = []
    for doc in documents:
        record = dict(doc)
        records.append(record)
    return render_template('stats.html', records=records)

if __name__ == "__main__":
    app.run(debug=True)