from flask import Flask, render_template, request
from openai import OpenAI
import os

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key here
API_KEY = os.getenv("CUSTOMER_SUPPORT_BOT_API_KEY")
client = OpenAI(api_key=API_KEY)

# Define a function that interacts with GPT-3.5/4 API
def get_bot_response(user_query):
    response = client.chat.completions.create(
        model="gpt-4", # You can also use "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": user_query}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    bot_response = response.choices[0].message.content.strip()
    return bot_response

# Define the main route for the bot interface
@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        user_query = request.form["user_query"]
        bot_response = get_bot_response(user_query)
        return render_template("index.html", user_query=user_query, bot_response=bot_response)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)