from flask.cli import FlaskGroup
from app import app, db

# Agregar grupo de comandos
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('created')


@cli.command("setup")
def setup():
    create_db()


if __name__ == '__main__':
    cli()
