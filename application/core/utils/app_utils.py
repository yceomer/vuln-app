from application.core.db_models import MobileApplication
from application.core.app_models import BaseResponse


class AppUtils:
    @staticmethod
    def get_filter_app(search_text):
        response = BaseResponse()
        if search_text.startswith('com'):
            response = MobileApplication.query.filter_by(application_id=search_text.lower()).first()
        else:
            response = MobileApplication.query.filter(MobileApplication.application_name.like(f'%{search_text}%')).first()
        return response.__dict__


