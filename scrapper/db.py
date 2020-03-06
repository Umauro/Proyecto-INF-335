import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

USER_DATA = {
    'user': 'postgres',
    'password': 'admin'
}

BD_DATA = {
    'host': 'localhost',
    'database': 'tablegames',
    'port': '5432'
}

def get_psycopg2_connection(user_data, db_data):
    """
    Entrega una conexión a la base de datos presente en db_data,
    considerando el usuario en user_data

    :param user_data: Diccionario con los datos de conexión del usuario
    :param db_data: Diccionario con los datos de conexión de la base de datos
    :return: psycopg2 connection
    """
    try:
        conn = psycopg2.connect(user=user_data['user'],
                                password=user_data['password'],
                                host=db_data['host'],
                                port=db_data['port'],
                                database=db_data['database'])
        return conn
    except Exception as error:
        print("Error al conectarse a la BD \n {}".format(error))
        return None
    
def do_sql_upsert(user_data, db_data, upsert_query):
    """

    :param user_data: Diccionario con los datos de conexión del usuario
    :param db_data: Diccionario con los datos de conexión de la bd
    :param upsert_query: Upsert Query
    :return:
    """
    try:
        conn = get_psycopg2_connection(user_data, db_data)
        cur = conn.cursor()
        cur.execute(upsert_query)
        conn.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        print(
            "Error en do_sql_upsert: {}".format(
                repr(error)
            )
        )
        return None
    finally:
        cur.close()
        conn.close()

def get_sql_alchemy_engine(user_data, db_data):
    """
        Retorna una engine de SqlAlchemy

    :param user_data: Diccionario con los datos del usuario
    :param db_data: Diccionario con los datos de la base de datos
    :return: Sqlalchemy Engine
    """
    try:
        engine = create_engine(
            URL(
                'postgresql+psycopg2',
                username=user_data['user'],
                password=user_data['password'],
                host=db_data['host'],
                port=db_data['port'],
                database=db_data['database']
            )
        )
        return engine
    except Exception as error:
        print("Error al generar un engine: {}".format(repr(error)))
        return None