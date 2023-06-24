from marshmallow import fields
from application import ma
from application.core.db_models import MobileApplication


class MobileApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MobileApplication
