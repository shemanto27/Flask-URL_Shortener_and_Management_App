from flask import Flask, render_template, request
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
        })

        return render_template("base.html", short_url=short_url)

    return render_template("base.html")











if __name__ == "__main__":
    app.run(debug=True)