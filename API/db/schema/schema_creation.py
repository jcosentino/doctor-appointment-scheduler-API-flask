import sqlalchemy

def check_schema():
    engine = sqlalchemy.create_engine('mysql://root:8milerun@localhost')
    engine.execute("CREATE SCHEMA IF NOT EXISTS `doc_appt_schema`;")
    engine.execute("USE doc_appt_schema;")