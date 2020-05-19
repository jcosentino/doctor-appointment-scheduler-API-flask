import sqlalchemy

def check_schema(username, password, hostname, schema_name):
    engine_str = 'mysql://{usern}:{passw}@{hostn}' \
                 .format(usern=username, passw=password, hostn=hostname)
    engine = sqlalchemy.create_engine(engine_str)
    engine.execute("CREATE SCHEMA IF NOT EXISTS `{sch_nm}`;".format(sch_nm=schema_name))
    engine.execute("USE {sch_nm};".format(sch_nm=schema_name))