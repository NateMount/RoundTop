# [Routes - Src]

import sys
import roundtop.models.brokers

from flask import request
from roundtop import app
from roundtop.util import check_table, token_required
    
get_hook:callable = lambda table_id: getattr(
    sys.modules['roundtop.models.brokers'], 
    table_id.title()+'Hook'
)

@app.route('/<table_id>/make')
@check_table
@token_required
def make(table_id:str):
    get_hook(table_id).insert(**request.get_json())
    return {}

@app.route('/<table_id>/get/<i>')
@check_table
@token_required
def get(table_id:str, i:int):
    return get_hook(table_id).get(i)

@app.route('/<table_id>/get')
@check_table
@token_required
def select(table_id:str):
    if request.get_json() == {}:
        return get_hook(table_id).all()
    return get_hook(table_id).select(**request.get_json())

@app.route('/<table_id>/drop')
@check_table
@token_required
def drop(table_id:str):
    get_hook(table_id).delete(**request.get_json())
    return {}

@app.route('/<table_id>/update')
@check_table
@token_required
def update(table_id:str):
    get_hook(table_id).update(**request.get_json())
    return {}
