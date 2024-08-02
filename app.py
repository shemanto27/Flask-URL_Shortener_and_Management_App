# from flask import Flask, render_template
# import pymongo
from hashids import Hashids

# app = Flask(__name__)

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["URL_Shortener"]
# collection = db["All_URLs"]
# collection.insert_one(dictionary)

# def url_shortener(URL):
generated_hashid = Hashids(salt="hello", min_length=4)
    # return generated_hashid

print("hello")
print(generated_hashid)






# @app.route('/')
# def home():
#     return render_template("base.html")

# if __name__ == "__main__":
#     app.run(debug=True)