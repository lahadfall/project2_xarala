# Utilisons l'héritage de la POO

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Solde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Classe de base pour les colonnes communes
class BaseModel(db.Model):
    __abstract__ = True  # Cette classe ne crée pas de table
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)

# Table Revenue
class Revenue(BaseModel):
    __tablename__ = 'Revenue'

# Table Depense
class Depense(BaseModel):
    __tablename__ = 'Depense'
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables Revenue et Depense créées avec succès.")
        
            # Ajouter un Revenue
        nouveau_revenue = Revenue(titre="Salaire", montant=2500.0)
        db.session.add(nouveau_revenue)

        # Ajouter une Depense
        nouvelle_depense = Depense(titre="Loyer", montant=800.0)
        db.session.add(nouvelle_depense)

        # Sauvegarder les modifications
        db.session.commit()

        print("Revenue et Depense ajoutés avec succès !")
        

