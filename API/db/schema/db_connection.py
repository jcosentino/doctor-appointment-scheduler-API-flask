def initConnections(app, username, password, hostname, schema_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://{usern}:{passw}@{hostn}/{sch_nm}'\
            .format(usern=username, passw=password, hostn=hostname, sch_nm=schema_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turn off annoying message