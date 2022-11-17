from flask import Blueprint, request, jsonify
from ..service.diagnose_service import DiagnoseService

bp = Blueprint('main', __name__, url_prefix='/diagnose')


@bp.route('/<crop>', methods=['POST'])
def diagnose_controller(crop):

    if len(request.files['file'].filename) == 0:
        return {'message': "Please attach an image file."}, 400

    if crop not in ['pepper', 'bean', 'napa_cabbage', 'radish', 'green_onion']:
        return {'message': "Please check crop's name."}, 400

    diagnose_serivce = DiagnoseService()
    res = diagnose_serivce.predict(crop, request.files['file'])

    return res
