from application.core.utils.app_utils import AppUtils
from flask import request, abort
from application.userland.controller import mod_userland
import bleach


@mod_userland.route('/search', methods=['GET'])
def get_app_details():
    search_text = bleach.clean(request.args.get('searchText', ''))
    if search_text:
        response = AppUtils.get_filter_app(search_text)
        if response:
            return response
        else:
            return abort(500)
    else:
        return abort(500)