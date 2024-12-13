from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Solde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("CLE_SECRET_FLASK")


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

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        données = request.form
        titre = données.get("titre")
        montant = float(données.get('montant'))
        type_entry = données.get('type')  # On peut déterminer si c'est un revenu ou une dépense

        if type_entry == 'Revenue':
            new_titre = Revenue(titre=titre, montant=montant)  
            db.session.add(new_titre)
            db.session.commit()
        elif type_entry == 'Depense':
            new_titre = Depense(titre=titre, montant=montant)  # Idem pour la dépense
            db.session.add(new_titre)
            db.session.commit()
        
        flash("Enregistrement ajouté avec succès.", "success")
        return redirect(url_for('index'))
    else:
         # Récupérer les revenus et dépenses
        revenus = Revenue.query.order_by(Revenue.montant).all()
        depenses = Depense.query.order_by(Depense.montant).all()  
        
        total_revenus = sum(revenu.montant for revenu in revenus)
        total_depenses = sum(depense.montant for depense in depenses)
        
        # Définir un budget fixe ou dynamique
        budget = total_revenus  # Si le budget dépend des revenus
        solde = budget - total_depenses
        
        return render_template(
            'index.html', 
            revenus=revenus, 
            depenses=depenses,
            budget=budget, 
            total_depenses=total_depenses, 
            solde=solde
            )
    
    
@app.route("/delete_revenue/<int:id>/")
def delete_revenue(id):
    revenue = Revenue.query.get_or_404(id)
    try:
        db.session.delete(revenue)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Une erreur s'est produite: {e}"
    
@app.route("/delete_depense/<int:id>/")
def delete_depense(id):
    depense = Depense.query.get_or_404(id)
    try:
        db.session.delete(depense)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Une erreur s'est produite: {e}"

@app.route("/revenue")
def revenue():
    return render_template('form_revenue.html')

@app.route("/depense")
def depense():
    return render_template('form_depense.html')




if __name__ == '__main__':
    app.run(debug=True)






