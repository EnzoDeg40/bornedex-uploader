import os
from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import config as config

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config.discord_oauthlib_insecure_transport
app.config["DISCORD_CLIENT_ID"] = config.discord_client_id
app.config["DISCORD_CLIENT_SECRET"] = config.discord_client_secret
app.config["DISCORD_REDIRECT_URI"] = config.discord_redirect_uri

discord = DiscordOAuth2Session(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/home/")
@requires_authorization
def home():
    return render_template("home.html")

@app.route("/upload/", methods=["POST"])
@requires_authorization
def upload():
    user = discord.fetch_user()
    print(user.username)
    
    # Gérez le fichier image
    image = request.files['image']
    image.save("uploads/" + image.filename)
    
    return "okay"

@app.route("/login/")
def login():
    if discord.authorized:
        return redirect(url_for("home"))
    else:
        return discord.create_session()

@app.route('/logout/')
def logout():
    discord.revoke()
    return redirect(url_for('index'))

@app.route("/callback/")
def callback():
    try:
        discord.callback()
    except Exception as e:
        redirect(url_for("index"))
    return redirect(url_for("home"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))
	
# @app.route("/account/")
# @requires_authorization
# def me():
#     user = discord.fetch_user()
#     return f"""
#     <html>
#         <head>
#             <title>{user.name}</title>
#         </head>
#         <body>
#             <img src='{user.avatar_url}' />
#         </body>
#     </html>"""

if __name__ == "__main__":
    app.run(debug=True)