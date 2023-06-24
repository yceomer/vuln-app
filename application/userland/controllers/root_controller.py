from application.userland.controller import mod_userland
from flask import render_template


@mod_userland.route('/app', defaults={'path': ''})
@mod_userland.route('/app/<path:path>', methods=['GET', 'POST'])
def get_app_index(path):
    return render_template('app/index.html')
