from flask import Flask, render_template

from src.common.database import Database


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "41C7BC6A616734FC4EFBF2FA14091B4A6079347A1DB3F2A0A71427CC589E963A97" \
                 "879BA2AA8B6FC502937F0A0B0D286A4A8DBEAC83375681A6A38C21C9A38E73"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
