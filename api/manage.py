from flask.cli import FlaskGroup
from app import app
import db

# Agregar grupo de comandos
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.create_db()


if __name__ == '__main__':
    cli()
