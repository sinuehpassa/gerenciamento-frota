from src.models.models import Carro

class ServiceService():
    def __init__(self, db_session, current_user):
        self.db_session = db_session
        self.current_user = current_user
    
    def list_all(self):
        return self.db_session.query(Carro).all()
    
    def list_one(self, id):
        return self.db_session.query(Carro).filter_by(
            id=id,
            user_id=self.current_user.id # adicionar esse filtro se precisar limitar quem pode acessar
        ).first()

    def create(self, data):
        return Carro(**data, user_id=self.current_user.id)
    
    def save(self, carro):
        carro = self.create(carro)
        try:
            self.db_session.add(carro)
            self.db_session.commit()
            return carro
        except Exception as e:
            self.db_session.rollback()
            raise e
        
    def update(self, id, data):
        carro = self.list_one(id)
        
        if not carro:
            return None
        
        for key, value in data.items():
            setattr(carro, key, value)
        
        try:
            self.db_session.commit()
            return carro
        except Exception as e:
            self.db_session.rollback()
            raise e
        return carro
    
    def delete(self, id):
        carro = self.list_one(id)
        
        if not carro:
            return None
        
        try:
            self.db_session.delete(carro)
            self.db_session.commit()
            return carro
        except Exception as e:
            self.db_session.rollback()
            raise e