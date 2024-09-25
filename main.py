from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from openai import OpenAI

OpenAI.api_key = "sk-proj-3wB0V2WPsc4mTgxug1GOT3BlbkFJNq7VX3essg1XEGzYsEdh"
client = OpenAI()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Happykumar:happy%402004@ioclmongodb.kpsg2bh.mongodb.net/CHATBOT"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats = [chat for chat in chats]
    return render_template("index.html", mychats=mychats)

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        if chat:
            data = {"question": question, "answer": chat["answer"]}
            return jsonify(data)
        else:
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=question,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response["choices"][0]["text"]
            data = {"question": question, "answer": answer}
            mongo.db.chats.insert_one({"question": question, "answer": answer})
            return jsonify(data)
    data = {"result": "Thank you! I'm just a machine learning model designed to respond to questions and generate text based on my training data. Is there anything specific you'd like to ask or discuss? "}
    return jsonify(data)

app.run(debug=True)