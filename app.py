from flask import Flask

from flask_migrate import Migrate

from api.api import routes
from database.database import db


app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(routes, url_prefix='/star')

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=False)
