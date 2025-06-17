from flask import Flask, render_template, request
from classify import classify_image
import requests
import os
import markdown


app = Flask(__name__)

# Replace with your actual DeepSeek API key
API_KEY = API_KEY = os.environ.get("API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        image_path = os.path.join("static", "uploaded_image.jpg")
        image.save(image_path)

        condition = classify_image(image_path)
        advice_raw = get_deepseek_advice(condition)
        advice = markdown.markdown(advice_raw)


        return render_template("index.html", result=advice, condition=condition, image=image_path)

    return render_template("index.html", result=None)

def get_deepseek_advice(condition):
    prompt = f"What is {condition}? If the condition is normal,say that everything is good, and that you have a normal condition. ELSE  respond to this: What are possible causes, home treatments, and when should someone see a doctor?, "

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Error contacting  API. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
