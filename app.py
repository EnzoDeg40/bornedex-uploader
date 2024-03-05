import os
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import config as config
import sql as sql
import format as format

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = config.discord_oauthlib_insecure_transport
app.config["DISCORD_CLIENT_ID"] = config.discord_client_id
app.config["DISCORD_CLIENT_SECRET"] = config.discord_client_secret
app.config["DISCORD_REDIRECT_URI"] = config.discord_redirect_uri

discord = DiscordOAuth2Session(app)
db = sql.db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/home/")
@requires_authorization
def home():
    user = discord.fetch_user()
    bornes = db.get_user_bornes(user.id)
    return render_template("home.html", user=user, bornes=bornes, format=format)

@app.route("/map/")
def map():
    return render_template("map.html")

@app.route("/upload/", methods=["POST"])
@requires_authorization
def upload():
    if not all(key in request.form for key in ["lat", "lon"]):
        return jsonify({"error": "Missing required fields in the form data."}), 400
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    if request.files["image"].filename == "":	
        return jsonify({"error": "No selected file"}), 400
    
    user = discord.fetch_user()
    print(user.username)
    if not user:
        return jsonify({"error": "An error occurred while fetching your account."}), 500
    
    alt = request.form.get("alt", None)
    name = request.form.get("name", None)
    city = request.form.get("city", None)
    wiki = request.form.get("wiki", None)

    borne = sql.borne(None, None, name, request.form["lat"], request.form["lon"], alt, city, wiki, user.id, user.username, user.email, user.avatar_url, None)
    borne_id = db.insert_borne(borne)
    if borne_id is None:
        return jsonify({"error": "An error occurred while creating the borne."}), 500
    
    image = request.files['image']
    image.save("uploads/" + str(borne_id) + ".jpg")
    if not os.path.exists("uploads/" + str(borne_id) + ".jpg"):
        return jsonify({"error": "An error occurred while saving the image."}), 500

    return jsonify({"success": "Borne created successfully."}), 201

@app.route("/login/")
def login():
    if discord.authorized:
        return redirect(url_for("home"))
    else:
        return discord.create_session()

@app.route('/list/')
def list():
    user = discord.fetch_user()
    bornes = db.get_user_bornes(user.id)
    return render_template("list.html", user=user, bornes=bornes, format=format)

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
    # app.run(debug=True, host="0.0.0.0", port=5000, ssl_context='adhoc')
    app.run(debug=True, host="0.0.0.0", port=5000)