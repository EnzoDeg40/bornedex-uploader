import os

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

import config as config

app = Flask(__name__)

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config.discord_oauthlib_insecure_transport
app.config["DISCORD_CLIENT_ID"] = config.discord_client_id
app.config["DISCORD_CLIENT_SECRET"] = config.discord_client_secret
app.config["DISCORD_REDIRECT_URI"] = config.discord_redirect_uri
app.config["DISCORD_BOT_TOKEN"] = config.discord_bot_token

discord = DiscordOAuth2Session(app)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <a href='/login/'>Login with Discord</a>
        </body>
    </html>"""

@app.route("/login/")
def login():
    return discord.create_session()

@app.route('/logout')
def logout():
    discord.revoke()
    return redirect(url_for('home'))
	

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

	
@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""


if __name__ == "__main__":
    app.run()