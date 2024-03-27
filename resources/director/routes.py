from flask import request, jsonify 
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required

from schemas import DirectorSchema, DirectorWithMovieSchema
from . import bp

# from db import director
from models.director_model import DirectorModel

@bp.route('/director')
class DirectorList(MethodView):
    
    @bp.response(200, DirectorWithMovieSchema(many=True))
    def get(self):
        return DirectorModel.query.all() 

    
    @bp.arguments(DirectorSchema)
    @bp.response(201, DirectorSchema)
    def post(self, data):

        try:
            director = DirectorModel()
            director.from_dict(data)
            director.save_director()
            return director
        except:
            abort(400, message="Director or email has already been taken. Please try a different one.")



@bp.route('/director/<int:id>')
class Director(MethodView):
    
    @bp.response(200, DirectorWithMovieSchema)
    def get(self, id):
        director = DirectorModel.query.get(id)
        if director:
            return director
        else:
            abort(400, msg='Not a valid entry')



    @bp.arguments(DirectorSchema)
    @bp.response(200, DirectorWithMovieSchema)
    def put(self, data, id):
        director = DirectorModel.query.get(id)
        if director:
            director.from_dict(data)
            director.save_director()
            return director
        else:
            abort(400, message='Not a valid entry')
     


    def delete(self, id):
        director = DirectorModel.query.get(id)
        if director:
            director.del_director()
            return {'Message': 'Director deleted'}, 200
        abort(400, message='Not a valid entry')
        


##### jwt 
        
@bp.post('/login')
def login():
    login_data = request.get_json()

    username = login_data['username']
    director = DirectorModel.query.filter_by(username = username).first()
    if director and director.check_password(login_data['password']):
        access_token = create_access_token(identity=director.id)
        return {'access_token': access_token}, 201
    
    abort(Message="Invalid Director Data")

@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"Message": "Logout successful"})
    unset_jwt_cookies(response)
    return response
