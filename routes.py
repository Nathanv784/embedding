from flask import Blueprint, request, jsonify
from chat import uploaded_file
from db import db
main = Blueprint('main', __name__)
@main.route('/upload', methods=['POST'])
def upload_file():
    """
    _summary_

    Returns:
        _type_: _description_
    """
    response =  uploaded_file(db)
    return jsonify(response)