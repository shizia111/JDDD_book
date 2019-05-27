import json

from flask import render_template, request

from record.helper import JDDD
from record.views import admin


@admin.route('/')
def index():
    return render_template('index.html')


@admin.route('/search', methods=['POST'])
def serch():
    gjz = request.form.get('gjz').strip() if request.form.get('gjz') else ''

    pt = request.form.get('pt').strip() if request.form.get('pt') else ''

    l = JDDD(gjz)
    if pt == '京东':
        data = [i for i in l.JD()]

        return json.dumps({'code': 0, 'msg': data})
    elif pt == '当当':
        data = [i for i in l.dangdang()]

        return json.dumps({'code': 0, 'msg': data})
    else:
        data = [i for i in l.JD()] + [i for i in l.dangdang()]

        return json.dumps({'code': 0, 'msg': data})
