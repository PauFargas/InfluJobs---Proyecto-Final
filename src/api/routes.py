"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_cors import CORS
from api.models import db, Users, UsersCompany, UsersInfluencers, Offers, OffersCandidates, SocialNetworks
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import datetime


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {}
    response_body["message"] = "Hello! I'm a message that came from the backend, check the network tab on the browser inspector and you will see the GET request"
    return response_body, 200


@api.route('/signup', methods=['POST'])
def signup():
    response_body = {}
    data = request.json
    user = Users(email = data.get('email'),
                 password = data.get('password'),
                 is_active = True,
                 is_influencer = data.get('is_influencer')
                 )
    user_exist = db.session.execute(db.select(Users).where(Users.email == user.email)).scalar()
    if user_exist:
        return jsonify({"message": "Usuario existente"}), 401
    db.session.add(user)
    db.session.commit()
    response_body['results'] = user.serialize()
    response_body['message'] = "Usuario creado"
    access_token = create_access_token(identity=[user.serialize()])
    response_body['access_token'] = access_token
    return response_body, 200


@api.route('/login', methods=["POST"])
def login():
    response_body = {}
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_influencer =  request.json.get("is_influencer", None)
    user = db.session.execute(db.select(Users).where(Users.email == email, Users.password == password, Users.is_active == True)).scalar()
    if not user:
        return jsonify({"message": "Bad email or password"})
    if user.is_influencer:
        user_influencer = db.session.execute(db.select(UsersInfluencers).where(UsersInfluencers.id_user == user.serialize()["id"])).scalar()
        data_serialize = user_influencer.serialize()
    else:
        user_company = db.session.execute(db.select(UsersCompany).where(UsersInfluencers.id_user == user.serialize()["id"])).scalar()
        data_serialize = user_company.serialize()
    access_token = create_access_token(identity=[user.serialize(), data_serialize])
    response_body["message"] = "Login"
    response_body["results"] = {"user": user.serialize(), "profile": data_serialize}
    response_body["access_token"] = access_token
    return response_body, 200
  

@api.route('/private', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def private():
    if request.method == "GET":
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"message": "Access denied"}), 401
        if current_user[0]['is_influencer'] == True: 
            response_body = {}
            response_body["message"] = "Perfil del influencer"
            response_body["results"] = current_user
            return response_body, 200
        if current_user[0]['is_influencer'] == False:
            response_body = {}
            response_body["message"] = "Perfil del Empresario"
            response_body["results"] = current_user
            return response_body, 200
    if request.method == "PUT":
        current_user = get_jwt_identity()
        response_body = {}
        results = {}
        data = request.json
        if not current_user:
            return jsonify({"message": "Access denied"}), 401
        user = db.session.execute(db.select(Users).where(Users.email == current_user[0]["email"])).scalar()
        user.password = data.get('password')
        db.session.commit()
        results['user'] = user.serialize()
        response_body['message'] = 'Usuario modificado'
        response_body['results'] = results
        return response_body, 200
    if request.method == "DELETE":
        current_user = get_jwt_identity()
        response_body = {}
        user = db.session.execute(db.select(Users).where(Users.id == current_user[0]["id"])).scalar()
        if not user:
            response_body['message'] = 'Usuario inexistente'
            return response_body, 400
        if current_user[0]['is_influencer'] == True:
            user_profile = db.session.execute(db.select(UsersInfluencers).where(UsersInfluencers.id_user == current_user[0]["id"])).scalar()
            db.session.delete(user)
            db.session.delete(user_profile)
            db.session.commit()
            response_body['message'] = 'Usuario eliminado'
            return response_body, 200
        if current_user[0]['is_influencer'] == False:
            user_profile = db.session.execute(db.select(UsersCompany).where(UsersCompany.id_user == current_user[0]["id"])).scalar()
            db.session.delete(user)
            db.session.delete(user_profile)
            db.session.commit()
            response_body['message'] = 'Usuario eliminado'
            return response_body, 200


@api.route('/profile', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def profile():
    if request.method == "GET":
        current_user = get_jwt_identity()
        response_body = {}
        if not current_user:
            return jsonify({"message": "Bad email or password"}), 401
        if current_user[0]['is_influencer'] == True: 
            user = db.session.execute(db.select(UsersInfluencers).where(UsersInfluencers.id_user == current_user[0]["id"])).scalar()
            response_body["message"] = "Perfil del influencer"
            if not user:
                response_body["results"] = user
                return response_body, 200
            response_body["results"] = user.serialize()
            return response_body, 200
        if current_user[0]['is_influencer'] == False:
            user = db.session.execute(db.select(UsersCompany).where(UsersCompany.id_user == current_user[0]["id"])).scalar()
            response_body["message"] = "Perfil del Empresario"
            if not user:
                response_body["results"] = user
                return response_body, 200
            response_body["results"] = user.serialize()
            return response_body, 200
    if request.method == "POST":
        current_user = get_jwt_identity()
        response_body = {}
        if not current_user:
            return jsonify({"message": "Bad email or password"}), 401
        if current_user[0]['is_influencer'] == True: 
            data = request.json
            user = UsersInfluencers(first_name = data.get('first_name'),
                                    last_name = data.get('last_name'),
                                    date_birth = datetime.now(), ## Esto no supe como agregar la fecha de nacimiento, asique puse para que tire la fecha actual, hay que revisarlo
                                    gender = data.get('gender'),
                                    telephone = data.get('telephone'),
                                    country = data.get('country'),
                                    zip_code = data.get('zip_code'),
                                    profile_img = data.get('profile_img'),
                                    headline = data.get('headline'),
                                    description = data.get('description'),
                                    social_networks = data.get('social_networks'),
                                    id_user = current_user[0]['id']
                                    )
            db.session.add(user)
            db.session.commit()
            response_body['user'] = user.serialize()
            return response_body, 200
        if current_user[0]['is_influencer'] == False:
            data = request.json
            user = UsersCompany(name = data.get('name'),
                                cif = data.get('cif'),
                                country = data.get('country'),
                                zip_code = data.get('zip_code'),
                                telephone = data.get('telephone'),
                                headline = data.get('headline'),
                                description = data.get('description'),
                                industry = data.get('industry'),
                                profile_img = data.get('profile_img'),
                                website = data.get('website'),
                                id_user = current_user[0]['id']
                                )
            db.session.add(user)
            db.session.commit()
            response_body['user'] = user.serialize()
            return response_body, 200
    if request.method == "PUT":
        current_user = get_jwt_identity()
        response_body = {}
        if not current_user:
            return jsonify({"message": "Bad email or password"}), 401
        if current_user[0]['is_influencer'] == True: 
            data = request.json
            users_influencers = db.session.execute(db.select(UsersInfluencers).where(UsersInfluencers.id_user == current_user[0]["id"])).scalar()
            if not users_influencers:
                return jsonify({"message:" "Usuario no encontrado"}), 404
            users_influencers.first_name = data.get('first_name')
            users_influencers.last_name = data.get('last_name')
            ## users_influencers.date_birth = data.get('date_birth')
            users_influencers.gender = data.get('gender') 
            users_influencers.telephone = data.get('telephone')
            users_influencers.country = data.get('country')
            users_influencers.zip_code = data.get('zip_code')
            users_influencers.profile_img = data.get('profile_img')
            users_influencers.headline = data.get('headline')
            users_influencers.description = data.get('description')
            users_influencers.social_networks = data.get('social_networks')
            db.session.commit()
            response_body['user'] = users_influencers.serialize()
            response_body['message'] = 'El usuario ha sido modificado'
            return response_body, 200
        if current_user[0]['is_influencer'] == False:
            data = request.json
            users_company = db.session.execute(db.select(UsersCompany).where(UsersCompany.id_user == current_user[0]["id"])).scalar()
            if not users_company:
                return jsonify({"message:" "Empresa no encontrada"}), 404
            users_company.name = data.get('name')
            users_company.country = data.get('country')
            users_company.zip_code = data.get('zip_code') 
            users_company.telephone = data.get('telephone')
            users_company.headline = data.get('headline')
            users_company.description = data.get('description')
            users_company.industry = data.get('industry')
            users_company.profile_img = data.get('profile_img')
            users_company.website = data.get('website')
            db.session.commit()
            response_body['user'] = users_company.serialize()
            response_body['message'] = 'Los datos de la empresa han sido modificados'
            return response_body, 200


@api.route('/offers', methods=['GET'])
def offers():
    response_body = {}
    results = {}
    offers = db.session.execute(db.select(Offers)).scalars()
    list_offers = []
    for row in offers:
        list_offers.append(row.serialize())
    results['offers'] = list_offers
    response_body['message'] = 'Listado de ofertas'
    response_body['results'] = results
    return response_body, 200

    
@api.route('/offers/<int:id_user_company>/<int:offers_id>', methods=['PUT', 'DELETE'])  # SOLO PARA USERS/COMPANY
@jwt_required()
def private_offer_singular(offers_id):
    if request.method == 'DELETE':
        current_user = jwt_required
        response_body = {}
        if current_user[0]['is_influencer'] == False:
            user_offer = db.session.execute(db.select(Offers).where(Offers.id == offer_id, Offers.id_company == current_user[0]["id"])).scalar()
            db.session.delete(user_offer)
            db.session.commit()
            response_body['message'] = 'Oferta eliminada'
            return response_body, 200
    if request.method == 'PUT':
        current_user = jwt_required()
        if not current_user:
            return jsonify({"message": "Access denied"}), 401
        if current_user[0]['is_influencer'] == False:
             data = request.json
        user_offer = db.session.execute(db.select(Offers).where(Offers.id == offer_id, Offers.id_company == current_user[0]["id"])).scalar()
        if not user_offers:
                return jsonify({"message:" "No se han encontrado ofertas"}), 404
        user_offer.title = data.get('title') 
        user_offer.post = data.get('post')
        user_offer.date_publish = data.get('date_publish')
        user_offer.status = data.get('status')
        user_offer.salary_range = data.get('salary_range')
        user_offer.min_followers = data.get('min_followers')
        user_offer.duration_in_weeks = data.get('duration_in_weeks')
        user_offer.location = data.get('location') 
        user_offer.industry = data.get('industry')
        db.session.commit()
        response_body['offer: '] = user_offer.serialize()
        response_body['message'] = 'Los datos de la oferta han sido modificados'
        return response_body, 200  
         

@api.route('/offer-candidates', methods=['GET', 'POST'])
@jwt_required()
def offer_candidates():
    response_body = results = {}
    if request.method == 'POST':
        current_user = get_jwt_identity()
        if current_user[0]['is_influencer'] == False: 
            response_body["message"] = "Acceso denegado, no tiene perfil de influencer"
            response_body["results"] = current_user
            return response_body, 401
        # Aqui debo hacer la logica para que un influencer aplique a una oferta.
        if current_user[0]['is_influencer'] == True:
            data = request.json
            offer_register = OffersCandidates(status = "pending", 
                                              status_influencer = "active",
                                              cover_letter = data.get('cover_letter'),
                                              social_network_url = data.get('social_network_url'),
                                              followers = data.get('followers'),
                                              id_offer = data.get('id_offer'),
                                              id_influencer = current_user[1]['id'])
        db.session.add(offer_register)
        db.session.commit()
        response_body['Registrado: '] = offer_register.serialize()                 
        # Obtener los datos del json de lo que me estan enviando
        return response_body, 200


@api.route('/offer-candidates/<int:id>', methods=['GET', 'DELETE'])
@jwt_required()
def offer_candidates_id(id):
    response_body = results = {}
    response_body["results"] = results
    # Buscamos en la base si esa oferta existe
    offer_candidates = db.session.execute(db.select(OffersCandidates).where(OffersCandidates.id == id)).scalar()
    # Si no existe, hacemos un return devolviendo el error al front
    if not offer_candidates:
        response_body["message"] = "No existe la oferta solicitada"
        return response_body, 404
    current_user = get_jwt_identity()
    if current_user[0]['is_influencer'] == False:
        response_body["message"] = "Acceso denegado, no tiene perfil de influencer" 
        return response_body, 403
    if current_user[1]['id'] != offer_candidates.serialize()['id_influencer']:
        response_body["message"] = "Esta publicacion no corresponde al perfil"
        return response_body, 404
    if request.method == 'GET':
        # TODO: una compañia podra ver este endpoint?
        response_body['message: '] = "Datos de la postulacion"  
        results = offer_candidates.serialize()         
        response_body['results'] = results
        return response_body, 200
    if request.method == 'DELETE':
        # Eliminar la oferta de ese ID
        offer_candidates["status_influencer"] = 'inactive'
        db.session.commit()
        response_body['message: '] = "Oferta anulada"  
        results = offer_candidates.serialize()          
        response_body['results'] = results
        return response_body, 200


@api.route('/influencers/<int:id>/offer-candidates', methods=['GET'])
@jwt_required()
def offer_candidates_by_influencer(id):
    response_body = results = {}
    response_body["results"] = results
    if request.method == 'GET':
        # Muestro todas las ofertas que se postulo el influencer.
        current_user = get_jwt_identity()
        # Ver las ofertas ID de ese candidato  
        if current_user[0]['is_influencer'] == False:
            response_body["message"] = "Acceso denegado, no tiene perfil de influencer" 
            return response_body, 403
        if current_user[1]['id'] != id:
            response_body["message"] = "Acceso denegado, no tiene perfil de influencer" 
            return response_body, 403
        offers = db.session.execute(db.select(OfferCandidates).where(OffersCandidates.id_influencer == id)).scalars()
        offers_list = []
        for row in offers:
            offers_list.append(row.serialize())
        results['offers'] = offers_list
        response_body['message'] = "Ofertas"            
        response_body['results'] = results
        return response_body, 200

