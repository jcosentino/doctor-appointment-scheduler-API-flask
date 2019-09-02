def initConnections(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8milerun@localhost/doc_appt_schema'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turn off annoying message