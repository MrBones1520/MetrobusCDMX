from db import db
from model import CDMX

cdmx = CDMX()


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('created Tables')


def create_date_base():
    db.session.add_all(cdmx.alcaldias)
    db.session.commit()
    print("Created Alcaldias")
