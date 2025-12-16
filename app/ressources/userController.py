from flask_restx import Namespace, Resource, fields, abort
from flask import request, json, current_app
from app.models.user import User, Profil
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, create_refresh_token

from ..config.pattern import is_valid_email, is_valid_password

api  = Namespace('utilisateur', description="Service gestion des utilisaters")

signup_model  = api.model(
    'signup',
    {
        'username': fields.String(required=True),
        'password': fields.String(required=True,
            description="Min 8 caractères, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial"),
        'nom': fields.String(required=True),
        'prenom': fields.String(required=True),
        'adresse': fields.String(required=True),
        'telephone': fields.String(required=True),
        'email': fields.String(required=True),
        "profils": fields.List(fields.String)
    }
)


login_model  = api.model(
    'login',
    {
        'username': fields.String(required=True),
        'password': fields.String(required=True)
    }
)

user_model = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'role': fields.String
})

user_model_update = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
})


@api.route("/signup")
class Signup(Resource):
    @api.expect(signup_model)
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def post(self):
        data  = api.payload
        profil = data.get("profils", [])
        if User.query.filter_by(username=data['username']).first():
            current_app.logger.warning(f"Echec: data{data['username']}")
            return {
                "message":"Utilisateur existe deja!!"
            }, 400
        if not is_valid_email(data['email']):
            abort(400, "Format email invalide") 

        if not is_valid_password(data['password']):
            abort(
                400,
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule, un chiffre et un caractère spécial"
                )
        new_user  = User(
            nom=data['nom'],
            prenom=data['prenom'],
            adress=data['adresse'],
            telephone=data['telephone'],
            email=data['email'],
            username=data['username'],
            password =User.generate_hash(data['password'])
        )
        for profil_libele in profil:
            profil = Profil.query.filter_by(libelle=profil_libele).first()
            if profil:
                new_user.profils.append(profil)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"succes: data{data['username']}")
        return {
            "message":"Utilisateur a été crée avec succés !!",
            "data":new_user.to_dict()
        } ,200

@api.route("/signin")
class Signin(Resource):
    @api.expect(login_model)
    def put(self):
        data = api.payload

        user = User.query.filter_by(username=data['username']).first()

        if not user or not User.verify_hash(data['password'], user.password):
            return {
                'message': 'Invalide password ou username'
            }, 401

        token = create_access_token(identity=str(user.id))
        refresh_token  = create_refresh_token(token)

        return {
            'message': 'Authentification réussie',
            'access_token': token,
            'refresh_token':refresh_token
        }, 200

    

@api.route("/update/<int:user_id>")
class UpdateUser(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.expect(user_model_update)
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            current_app.logger.warning(f"Echec: {user_id}")
            return {
                'message':"L\'utilisateur est introuvable !!"
            }
        data = api.payload
        user.username = data['username']
        user_update  = [{
            'id':user.id,
            "username":user.username
        }

        ]
        db.session.commit()
        return {'message':'Utilisateur est modifié avec succés ! !', 'user':user_update}, 200
    


@api.route("/delete/<int:user_id>")
class UpdateUser(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {
                'message':"L\'utilisateur est introuvable !!"
            }
        db.session.delete(user)
        db.session.commit()
        return {'message':'Utilisateur est supprimé avec succés ! !'}, 200


@api.route("/list_users")
class GetList(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self):
        list_user = User.query.all()
        list_useres = []
        for user in list_user:
            user = {
                "id":user.id,
                "username":user.username,
                "prenom":user.prenom,
                "nom":user.nom,
                "adresse":user.adress,
                "telephone":user.telephone,
                "email":user.email,
                "profil": [profil.libelle for profil in user.profils] 
            }
            list_useres.append(user)
        current_app.logger.info(f"Recuperation des utilisateurs: {list_useres}")
        return { 
            "message":"Liste des users recuperés avec succés !!sss",
            "users":list_useres}, 200
