from db import db
import model


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('created Tables')


def create_data(cdmx: model.CDMX):
    create_db()
    db.session.add_all(cdmx.alcaldias_model)
    print("Created Alcaldias")
    db.session.add_all(cdmx.linea_metrobus_model)
    print("Created Lineas del metro")
    db.session.commit()

