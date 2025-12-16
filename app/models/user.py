from ..extensions import db, bcrypt
from datetime import datetime



class UserProfil(db.Model):
    __tablename__ ="user_profil"

    id = db.Column(db.Integer, primary_key =True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_profil = db.Column(db.Integer, db.ForeignKey("profil.id"))

class Profil(db.Model):
    __tablename__ ="profil"
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    users = db.relationship("User", secondary="user_profil", back_populates="profils")




class User(db.Model):
    __tablename__ ="user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    prenom = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(128), nullable=False)
    adress = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    profils = db.relationship("Profil", secondary="user_profil", back_populates="users")

    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    

    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.check_password_hash(hashed, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "profil": [r.libelle for r in self.profils]
        }