from app import app
from models import db, Cupcake

with app.app_context():
    print("Is application context active?", app.app_context().g)  # This should not raise an error

    db.drop_all()
    db.create_all()

    c1 = Cupcake(
        flavor="cherry",
        size="large",
        rating=5,
    )

    c2 = Cupcake(
        flavor="chocolate",
        size="small",
        rating=9,
        image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
    )

    db.session.add_all([c1, c2])
    db.session.commit()
