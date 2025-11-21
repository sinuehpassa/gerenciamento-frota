from marshmallow import Schema, fields, validate
from marshmallow.fields import BytesField

class SchemaSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    date = fields.DateTime()
    active = fields.Bool()
    email = fields.Email(required=True)

class VehicleSchema(Schema):
    id = fields.Int(dump_only=True)
    plate = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    model = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    year = fields.Int(required=True)
    status = fields.Str(validate=validate.Length(max=20))
    criado_em = fields.DateTime()
    
class VehicleRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    request_date = fields.DateTime()
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    purpose = fields.Str(required=True)
    status = fields.Str(validate=validate.Length(max=20))
    return_date = fields.DateTime(allow_none=True)
    approved_by = fields.Int(allow_none=True)
    pickup_time = fields.Time(allow_none=True)
    return_time = fields.Time(allow_none=True)
    authorized_by_name = fields.Str(allow_none=True, validate=validate.Length(max=100))
    km_inicial = fields.Int(allow_none=True)
    km_final = fields.Int(allow_none=True)
    data_request = fields.DateTime(dump_only=True)
    
class VehicleInspectionSchema(Schema):
    id = fields.Int(dump_only=True)
    vehicle_id = fields.Int(required=True)
    request_id = fields.Int(allow_none=True)
    inspector_id = fields.Int(required=True)
    inspection_date = fields.DateTime()

    # Dados básicos
    current_mileage = fields.Int(required=True)
    fuel_level = fields.Str(required=True)

    # Itens de funcionamento
    foot_brake = fields.Str(required=True)
    foot_brake_obs = fields.Str(allow_none=True)
    parking_brake = fields.Str(required=True)
    parking_brake_obs = fields.Str(allow_none=True)
    starter_motor = fields.Str(required=True)
    starter_motor_obs = fields.Str(allow_none=True)
    wiper = fields.Str(required=True)
    wiper_obs = fields.Str(allow_none=True)
    washer = fields.Str(required=True)
    washer_obs = fields.Str(allow_none=True)
    toll_transponder = fields.Str(required=True)
    toll_transponder_obs = fields.Str(allow_none=True)
    headlights = fields.Str(required=True)
    headlights_obs = fields.Str(allow_none=True)
    front_turn_signals = fields.Str(required=True)
    front_turn_signals_obs = fields.Str(allow_none=True)
    rear_turn_signals = fields.Str(required=True)
    rear_turn_signals_obs = fields.Str(allow_none=True)
    brake_lights = fields.Str(required=True)
    brake_lights_obs = fields.Str(allow_none=True)
    reverse_lights = fields.Str(required=True)
    reverse_lights_obs = fields.Str(allow_none=True)
    internal_cleanliness = fields.Str(required=True)
    internal_cleanliness_obs = fields.Str(allow_none=True)
    dashboard_indicators = fields.Str(required=True)
    dashboard_indicators_obs = fields.Str(allow_none=True)
    radio = fields.Str(required=True)
    radio_obs = fields.Str(allow_none=True)
    tracker = fields.Str(required=True)
    tracker_obs = fields.Str(allow_none=True)

    # Itens de posse
    warning_triangle = fields.Str(required=True)
    jack = fields.Str(required=True)
    wheel_wrench = fields.Str(required=True)

    # Condições dos pneus
    tire_condition = fields.Str(required=True)
    spare_tire = fields.Str(required=True)

    # Condições da carroceria
    windows = fields.Str(required=True)
    doors = fields.Str(required=True)
    front_bumper = fields.Str(required=True)
    rear_bumper = fields.Str(required=True)
    body = fields.Str(required=True)
    mirrors = fields.Str(required=True)

    # Níveis de fluidos
    oil_level = fields.Str(required=True)
    brake_fluid = fields.Str(required=True)
    water_level = fields.Str(required=True)

    # Verificações adicionais
    valid_license = fields.Str(required=True)
    preventive_maintenance = fields.Str(required=True)
    has_leaks = fields.Str(required=True)

    # Campos legados
    exterior_condition = fields.Str(allow_none=True)
    interior_condition = fields.Str(allow_none=True)
    tire_condition_old = fields.Str(allow_none=True)
    lights_working = fields.Bool(allow_none=True)
    brakes_working = fields.Bool(allow_none=True)
    has_scratches = fields.Bool(allow_none=True)
    has_dents = fields.Bool(allow_none=True)

    observations = fields.Str(allow_none=True)
    inspection_type = fields.Str(required=True)
    data_request = fields.DateTime(dump_only=True)