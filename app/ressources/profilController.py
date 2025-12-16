from flask_restx import Namespace, Resource, fields
from flask import request, json
from app.models.user import User, Profil
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

api  = Namespace('Profils', description="Service gestion des profils")


@api.route("/list_profils")
class GetList(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self):
        lists_profils = Profil.query.all()
        list_profils = []
        for profil in lists_profils:
            profil = {
                "id":profil.id,
                "libelle":profil.libelle,
            }
            list_profils.append(profil)
        return { 
            "message":"Liste des users recuperés avec succés !!sss",
            "users":list_profils}, 200