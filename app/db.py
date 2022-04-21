#from flask_sqlalchemy import SQLAlchemy

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)


# class AlcaldiaModel(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     id_town = db.Column(db.Integer, unique=True, nullable=False)
#
#     def __init__(self, alcaldia: man.Alcaldia):
#         self.name = alcaldia.name
#         self.id_town = alcaldia.id_town
#
#
# class LineaMetroModel(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(80), unique=True, nullable=False)
#     simple_name = db.Column(db.String(80), unique=True, nullable=False)
#
#     def __init__(self, linea_metro: man.LineaMetro):
#         self.full_name = linea_metro.full_name
#         self.simple_name = linea_metro.simple_name