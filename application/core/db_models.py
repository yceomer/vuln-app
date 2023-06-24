from application import db


class MobileApplication(db.Model):
    __tablename__ = 'mobile_application'
    id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(), nullable=False)
    application_id = db.Column(db.String(), nullable=False, index=True)
    app_description = db.Column(db.String())
    app_requirements = db.Column(db.String())
    app_download_url = db.Column(db.String())
    app_category = db.Column(db.String(), index=True)
    app_img = db.Column(db.String())
    app_update_date = db.Column(db.DateTime())
    app_insert_date = db.Column(db.DateTime())
