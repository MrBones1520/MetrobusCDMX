

class AlcaldiaModel(db.Model):
    __tablename__ = "alcaldias"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    id_town = db.Column(db.Integer, unique=True, nullable=False)


class LineaMetroModel(db.Model):
    __tablename__ = "metrobus_lineas"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    simple_name = db.Column(db.String(80), unique=True, nullable=False)


class UnidadModel(db.Model):
    __tablename__ = "unidad"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    simple_name = db.Column(db.String(80), unique=True, nullable=False)
