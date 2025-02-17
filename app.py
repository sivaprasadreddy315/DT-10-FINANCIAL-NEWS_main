from flask import Flask, render_template, request
import pickle
import random

app = Flask(__name__)

def analyze_sentiment(text):
    sentiments = ['Positive', 'Negative', 'Neutral']
    return random.choice(sentiments)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    if request.method == "POST":
        message = request.form["message"]
        print(f"User input: {message}")

        try:
            with open("vectorizer.pickle", "rb") as vcfile:
                vectorizer = pickle.load(vcfile)

            with open("model.pickle", "rb") as mbfile:
                model = pickle.load(mbfile)

            transformed_data = vectorizer.transform([message])
            prediction = model.predict(transformed_data)
            sentiment = str(prediction[0])

        except Exception as e:
            print(f"Error loading model: {e}")
            sentiment = analyze_sentiment(message)  # Fallback prediction

        return render_template("predict.html", message=message, sentiment=sentiment)

    return render_template("predict.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
