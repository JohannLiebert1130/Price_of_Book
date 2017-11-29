from flask import Flask

from src.common.database import Database
from src.models.users.views import user_blueprint

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "41C7BC6A616734FC4EFBF2FA14091B4A6079347A1DB3F2A0A71427CC589E963A97" \
                 "879BA2AA8B6FC502937F0A0B0D286A4A8DBEAC83375681A6A38C21C9A38E73"


@app.before_first_request
def init_db():
    Database.initialize()


app.register_blueprint(user_blueprint, url_prefix="/users")
