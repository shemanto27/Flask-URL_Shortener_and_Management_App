from flask import Flask, render_template, request
import pymongo
from hashids import Hashids

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Random Secret Key'

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["URL_Shortener"]
# collection = db["All_URLs"]
# collection.insert_one(dictionary)

generated_hashid = Hashids(salt=app.config['SECRET_KEY'], min_length=4)



@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
    return render_template("base.html")











if __name__ == "__main__":
    app.run(debug=True)