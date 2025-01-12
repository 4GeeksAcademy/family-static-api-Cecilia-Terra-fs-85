"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object instanciando
jackson_family = FamilyStructure("Jackson") #instancia FamilyStructure

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#endpoints ejemplo GET devuelve todos los miembros de la familia
@app.route('/members', methods=['GET'])
def handle_hello():   
    members = jackson_family.get_all_members()
    response_body = {        
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)  #Traigo al miembro de la correpondiente ID
    if member:  #Si el miembro = a una ID devuelvo el miembro en formato json
        return jsonify(member), 200
    else:  
        return jsonify({"message": "Member not found"}), 404

    

@app.route('/member', methods=['POST']) #endpoints ejemplo POST agrega un nuevo miembro a la familia
def add_member():
    new_member = request.json
    jackson_family.add_member
   
    return jsonify(new_member), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])  # Endpoint bobba un mimnbo al cal representa una ID
def delete_member(member_id):  
    result = jackson_family.delete_member(member_id)  # Llamo a 'delete_member'    
    if result: #if resulto estoy valorarndo si la respuesta es true o false
        return jsonify({"message": "Member deleted successfully"}), 200  #llamo a la funciond delet en la clase familystructure por la id del miembro
    else:
        return jsonify({"message": "Member not found"}), 404  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
