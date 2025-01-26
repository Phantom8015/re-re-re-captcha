import os
import base64
import requests
from flask import Flask, request, render_template, redirect
from gradio_client import Client
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


client = Client("Phantom8015/martin-ha-toxic-comment-model")

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
html_template = "index.html"
falam_template = "index2.html"
url = "url"

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],
    storage_uri="memory://"
)

@app.route("/<path:encoded_url>", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def redirect_to_url(encoded_url):
    try:
        decoded_url = base64.b64decode(encoded_url).decode()
        text = ""
        if request.method == "POST":
            user_text = request.form.get("user_text", "")
            if user_text.strip():
                if user_text.lower() == "badder" or user_text.lower() == "filip" or user_text.lower() == "soydev":
                    text = "no"
                else:
                    result = client.predict(
                        param_0=user_text,
                        api_name="/predict"
                    )
                    print(result)
                    if result.get("label", "").lower() == "toxic":
                        text = "no"
                        return redirect(decoded_url)
                    else:
                        text = "yes"
                        return redirect("https://youtu.be/dQw4w9WgXcQ")
        return render_template(html_template, text=text)
    except Exception as e:
        print(f"Error: {e}")
        return redirect("/")

@app.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute")
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
    
    if url.strip():
        return render_template(falam_template, url=url, text="send that url to your friends!")
    else:
        return render_template(falam_template, url=url, text="")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
