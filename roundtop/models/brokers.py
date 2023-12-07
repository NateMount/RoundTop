# [Brokers - Models]

import sys
import roundtop.models

from roundtop.models import db

class NeoBroker():

    def __init__(self, table:object) -> None:
        self.table:object = table

    def insert(self, **kwargs) -> None:
        db.session.add(self.table(**kwargs))
        db.session.commit()
    
    def select(self, **filters) -> list:
        return [ 
            { k:d.__dict__[k] for k in d.__dict__ if not k.startswith('_')} for d in self.table.query.filter_by(**filters) 
        ]
    
    def all(self) -> list:
        return [ 
            { k:d.__dict__[k] for k in d.__dict__ if not k.startswith('_')} for d in self.table.query.all() 
        ]
    
    def delete(self, **filters) -> None:
        for data in self.table.query.filter_by(**filters).all():
            (db.session.delete(data), db.session.commit())
    
    def update(self, feature:str, val:object, **filters) -> None:
        for data in self.table.query.filter_by(**filters):
            (setattr(data, feature, val), db.session.commit())
    
    def get(self, element_id:int) -> dict:
        data:dict = self.table.query.get(element_id).__dict__
        return {k:data[k] for k in data if not k.startswith('_')}

[ 
    setattr(sys.modules[__name__], "{}Hook".format(table.__name__), NeoBroker(table)) for table in [
        getattr(
            sys.modules['roundtop.models'], 
            table
        ) for table in dir(sys.modules['roundtop.models']) if not '__' in table
    ][:-1] 
]

