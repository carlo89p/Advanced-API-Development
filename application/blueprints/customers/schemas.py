from extensions import db, ma
from models import Customer

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ('email', 'password')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()