from flask import Flask

from src.common.database import Database
from src.models.users.views import user_blueprint

app = Flask(__name__)
app.config.from_object('config')


@app.before_first_request
def init_db():
    Database.initialize()


app.register_blueprint(user_blueprint, url_prefix="/users")
