"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect

from models import db, connect_db, Cupcake

from forms import AddCupcakeForm

from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)
with app.app_context():
    db.create_all() 
   
@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddCupcakeForm()
    if form.validate_on_submit():
        new_cupcake = Cupcake(
            flavor=form.flavor.data,
            size=form.size.data,
            rating=form.rating.data,
            image=form.image.data or None
        )
        db.session.add(new_cupcake)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('index.html', form=form)
@app.route('/api/cupcakes')
def cupcake_data():
    """Gets data about all cupcakes"""
    all_cupcakes = [cupcake.serialized() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def data_single_cupcake(cupcake_id):
    """Gets data about a single cupcake"""
    single_cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=single_cupcake.serialized())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a cupcake with flavor, size, rating, and image"""
    json_data = request.get_json()  # Get the JSON data

    # Check if all fields are present
    if not json_data or not all(key in json_data for key in ['flavor', 'size', 'rating']):
        return jsonify({"error": "Missing data for required fields"}), 400

    # Attempt to create the Cupcake object
    try:
        create_cupcake = Cupcake(
            flavor=json_data['flavor'],
            size=json_data['size'],
            rating=json_data['rating'],
            image=json_data.get('image', None)  # Use get to provide a default of None if not specified
        )
        db.session.add(create_cupcake)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        return jsonify({"error": str(e)}), 400

    return jsonify(create=create_cupcake.serialized()), 201



@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Creates a cupcake with flavor, size, rating, and image"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image =request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialized())
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """ Deletes a single cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='Deleted')
