from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:ecovida@localhost:27017/ecovida?authSource=admin'
mongo = PyMongo(app)

with app.app_context():
    try:
        # Listar bases de datos
        print("Bases de datos:", mongo.cx.list_database_names())
        # Listar colecciones en la base de datos actual
        print("Colecciones:", mongo.db.list_collection_names())
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
