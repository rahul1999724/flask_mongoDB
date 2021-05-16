from bson import objectid
from flask import Flask, json
# pymongo is mogodb library
from flask_pymongo import PyMongo, pymongo
# bson.josn_util will convert bson to json
from bson.json_util import dumps
#bson.json_id will give random string
from bson.objectid import ObjectId
from flask import jsonify,request
#hashing library-> generate and check pwd
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

# connecting to MongoDB
app.config['MONGO_URI'] = "mongodb://localhost:27017/rahul"

#ORM

mongo = PyMongo(app)
print(mongo)


# create routr
# route for adding user
@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and request.method == 'POST':

        _hashed_password  = generate_password_hash(_password)

        id = mongo.db.rahul.insert({
            'name': _name,
            'email': _email,
            'pwd': _password 
        })

        resp = jsonify("User created Successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    resp = jsonify("wrong details")
    resp.status_code = 404
    return resp


# To display all users

@app.route('/users')
def users():
    users = mongo.db.rahul.find()
    resp = dumps(users)
    return resp



# To display info about specific user

@app.route('/user/<id>')
def user(id):
    user = mongo.db.rahul.find_one(
        {
            '_id': ObjectId(id)
        }
    )
    resp = dumps(user)
    return resp


# Delete operation

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.rahul.delete_one({
        '_id': ObjectId(id)
    })
    resp = jsonify("user deleted Successfully")
    resp.status_code = 200
    return resp


# Update Operation

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and _id and request.method == 'PUT':
        
        _hashed_password  = generate_password_hash(_password)

        mongo.db.rahul.update_one({
            '_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password
        }}
        )

        resp = jsonify("User Updated Successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found

# running the app
if __name__ == "__main__":
    app.run(debug=True)
