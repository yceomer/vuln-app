from application.utils.job_logger import job_logger
from application.utils.thirdparty.apkbe import Apkbe
from application.core.db_models import MobileApplication
from application import db
from application import create_app
from datetime import datetime


def check_apk_stores():
    logger = job_logger()

    logger.info('Check APK search is started.')

    apkbe = Apkbe(logger=logger)

    found_apps = apkbe.get_apkbe_apps()

    logger.info('Check APK search is finished.')
    app = create_app()
    with app.app_context():
        for found_app in found_apps:
            duplicate_control = MobileApplication.query.filter_by(application_id=found_app.get('application_id')).first()
            if not duplicate_control:
                app = MobileApplication(
                    application_name=found_app.get('title'),
                    application_id=found_app.get('application_id'),
                    app_img=found_app.get('app_img'),
                    app_description=found_app.get('description'),
                    app_requirements=found_app.get('requirements'),
                    app_category=found_app.get('category'),
                    app_download_url=found_app.get('download_url'),
                    app_update_date=datetime.strptime(found_app.get('updated'), '%Y-%m-%d'),
                    app_insert_date=datetime.now()
                )
                db.session.add(app)
                db.session.commit()
                logger.info(f'New app added, {found_app.get("title")}')
            else:
                logger.info(f'App already exists, {found_app.get("application_id")}')


if __name__ == '__main__':
    check_apk_stores()
