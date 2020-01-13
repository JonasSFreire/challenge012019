import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.api.models.users import User

app = create_app(os.environ.get('FLASK_CONFIG'))
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

@app.cli.command()
def deploy():
    upgrade()