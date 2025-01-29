import os
import base64
import random
import requests
from flask import Flask, request, render_template, redirect, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
app.secret_key = os.urandom(24)
html_template = "index.html"
falam_template = "index2.html"
url = "url"

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

@app.route("/", methods=["GET", "POST"])
@limiter.limit("100 per minute")
def addtosite():
    global url
    url = request.form.get("user_text", "")
    if url.strip():
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            if requests.get(url).status_code == 200:
                url = base64.b64encode(url.encode()).decode()
                url = "https://re-re-re-captcha.vercel.app/" + url  
        except requests.exceptions.RequestException:
            return render_template(falam_template, url="", text="site not found")
    
    return render_template(falam_template, url=url, text="send that url to your friends!" if url.strip() else "")

questions = [
    {"question": "what's the ultimate sigma grindset morning routine?", "options": ["come out as gay", "watching sigma tate", "gooning", "edging"], "answer": 2},
    {"question": "finish the phrase: 'skibidi _____'", "options": ["toilet", "sigma", "rizz", "balloon"], "answer": 0},
    {"question": "what does an ALPHA MALE do when rejected?", "options": ["cry", "GOON harder", "grind with sherry merry coo", "be gay"], "answer": 2},
    {"question": "what's the best haircut for MASSIVE rizz?", "options": ["bald", "low taper fade", "low aldi fade", "high taper fade"], "answer": 1},
    {"question": "who's the ultimate goon lord?", "options": ["gru", "the goon king", "kanye", "the WINNER"], "answer": 0},
    {"question": "gay?", "options": ["no.", "ily too", "slay", "haram"], "answer": 1},
    {"question": "Finish the phrase: 'I'm bouta _____'", "options": ["SWITCH TO ARCH LINUX", "EDGE", "GOON", "FEIN"], "answer": 3}
]

@app.route("/<path:encoded_url>", methods=["GET", "POST"])
@limiter.limit("100 per minute")
def redirect_to_url(encoded_url):
    try:
        decoded_url = base64.b64decode(encoded_url).decode()
        if "questions" not in session:
            session["questions"] = random.sample(questions, len(questions))
            session["current_question"] = 0
            session["correct_answers"] = 0
        
        if request.method == "POST":
            current_question = session["current_question"]
            user_answer = int(request.form.get("user_answer", -1))
            
            if user_answer == session["questions"][current_question]["answer"]:
                session["correct_answers"] += 1
            
            session["current_question"] += 1
            if session["current_question"] >= len(session["questions"]):
                score = session["correct_answers"]
                session.pop("questions", None)
                session.pop("current_question", None)
                session.pop("correct_answers", None)
                return render_template("index3.html", correct_answers=score, url=request.url)
        
        current_question = session["current_question"]
        return render_template(html_template, question=session["questions"][current_question], current_question=current_question, correct_answers=session["correct_answers"])
    except Exception as e:
        print(f"Error: {e}")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
