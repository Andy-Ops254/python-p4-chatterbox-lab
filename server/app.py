from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods =['GET', 'POST'])
def messages():
    if request.method=='GET':
        messages=[]
        for message in Message.query.order_by(Message.created_at.asc()).all():
            message_dict= message.to_dict()
            messages.append(message_dict)
        response = make_response(
            messages,
            200
        )
        return response

    elif request.method=='POST':
        new_message = Message(
        body = request.json.get("body"),
        username =request.json.get("username")
    )
    db.session.add(new_message)
    db.session.commit()

    messages_dict = new_message.to_dict()
    response = make_response(
        messages_dict,
        201
    )
    return response

@app.route('/messages/<int:id>', methods=['DELETE', 'PATCH'])
def messages_by_id(id):
    query = Message.query.filter_by(id=id).first()
    if request.method=='DELETE':
        db.session.delete(query)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "Message": "Message has been deleted successfully",
        }
        response = make_response(
            response_body,
            200
        )
        return response

    elif request.method=='PATCH':
        for attr in request.json:
            setattr(query, attr, request.json[attr])
        db.session.add(query)
        db.session.commit()
        query_dict = query.to_dict()
        response = make_response(
            query_dict,
            200
        )
        return response

if __name__ == '__main__':
    app.run(port=5555)
