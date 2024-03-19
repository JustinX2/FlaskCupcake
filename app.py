"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
from models import db, Cupcake, connect_db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='abc'

connect_db(app)

@app.route('/api/cupcakes')
def list_cupcakes():
    cupcakes=Cupcake.query.all()
    serialized=[c.serialize() for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake():
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data=request.json
    cupcake=Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None
    )
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()),201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    data=request.json
    cupcake.flavor=data.get('flavor', cupcake.flavor)
    cupcake.size=data.get('size', cupcake.size)
    cupcake.rating=data.get('rating', cupcake.rating)
    cupcake.image=data.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake=Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")