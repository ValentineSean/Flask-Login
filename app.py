from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine
from bson.objectid import ObjectId

import json

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
    "host": ""
}
app.config["SECRET_KEY"] = ""

db = MongoEngine()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Document):
    id_ = db.StringField()
    username = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    # return User.objects(id=ObjectId(user_id)).first()
    return User.objects(id=user_id).first()
    # return User.objects.get(id=user_id)

@app.route("/")
def index():
    user = User.objects(username="Valentine").first()
    login_user(user)
    return "You are now logged in!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are now logged out!"

@app.route("/home")
@login_required
def home():
    return "The current user is {}".format(current_user.username)

if __name__ == "__main__":
    app.run(debug=True)