from src.models.models import Vehicle

class CarService():
    def __init__(self, db_session, current_user):
        self.db_session = db_session
        self.current_user = current_user
    
    def list_all(self):
        return self.db_session.query(Vehicle).all()

    def register(self, data):
        return Vehicle(**data)

    def register_vehicle(self, data):
        vehicle = self.register(data)
        try:
            self.db_session.add(vehicle)
            self.db_session.commit()
            return vehicle
        except Exception as e:
            self.db_session.rollback()
            raise e
