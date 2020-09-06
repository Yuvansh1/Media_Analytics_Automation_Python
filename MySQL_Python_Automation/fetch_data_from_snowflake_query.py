from sqlalchemy import create_engine

engine =create_engine("****************************")

try:
    connection = engine.connect()
    results = connection.execute('select * from ******* limit 10').fetchone()
    print(results)
finally:
    connection.close()
    engine.dispose()