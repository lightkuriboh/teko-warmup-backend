
from hieupro.models.kuriboh import Kuriboh

db = Kuriboh.db


class Action(Kuriboh):
    __abstract__ = True
    @staticmethod
    def get_action_detail_by_id(random_id, model):
        return db.session.query(model).filter(model.random_id == random_id).first()
