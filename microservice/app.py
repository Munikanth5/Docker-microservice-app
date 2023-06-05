from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/api', methods=['GET'])
def api():
    users = User.query.all()
    data = [{'id': user.id, 'name': user.name} for user in users]
    return jsonify(data)

@app.route('/api/create', methods=['POST'])
def create_user():
    name = request.json['name']
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/api/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    
    new_name = request.json['name']
    user.name = new_name
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, host='0.0.0.0')

