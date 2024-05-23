from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    watermarks = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User {self.user_id} - Watermarks: {self.watermarks}>"


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id is None or not isinstance(user_id, int):
        return jsonify({'error': 'user_id is required and must be an integer'}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        new_user = User(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added', 'user_id': new_user.user_id}), 201
    else:
        return jsonify({'message': 'User already exists', 'user_id': user.user_id}), 200


@app.route('/watermarks', methods=['POST'])
def add_watermark():
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id is None or not isinstance(user_id, int):
        return jsonify({'error': 'user_id is required and must be an integer'}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id, watermarks=1)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User added and watermark added', 'user_id': user.user_id,
                        'total_watermarks': user.watermarks}), 201
    else:
        user.watermarks += 1
        db.session.commit()
        return jsonify(
            {'message': 'Watermark added', 'user_id': user.user_id, 'total_watermarks': user.watermarks}), 200


@app.route('/stats', methods=['GET'])
def get_stats():
    total_users = User.query.count()
    total_watermarks = db.session.query(db.func.sum(User.watermarks)).scalar() or 0
    return render_template('stats.html', total_users=total_users, total_watermarks=total_watermarks)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # app.run(debug=True)
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
