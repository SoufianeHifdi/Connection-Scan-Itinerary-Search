import sqlalchemy as db

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'database': 'ratp'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')# specify connection string


def connection_database():
	connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'# connect to database

	engine = db.create_engine(connection_str)

	connection = engine.connect()# pull metadata of a table

	metadata = db.MetaData(bind=engine)
	
	return engine,connection,metadata

#################################################### STOPS #############################################################

def search_stop(station_name,connection):
    query_sql = """SELECT stop_id,stop_name,parent_station FROM stops WHERE stop_name LIKE '%' :bar_tags '%' AND parent_station = '' """
    tags_res_list = connection.execute(db.text(query_sql), {"bar_tags": station_name}).fetchall()
    return tags_res_list

def get_stops(connection): 
    query_sql = "SELECT stop_id,stop_name FROM stops"
    res = connection.execute(db.text(query_sql))
    return res

#################################################### TRIPS #############################################################

def get_trips(connection):
    query_sql = "SELECT trip_id,trip_headsign,route_id FROM trips"
    res = connection.execute(db.text(query_sql))
    return res

#################################################### TRANSFERS #############################################################

def get_transfers(connection):
    query_sql = "SELECT * FROM transfers"
    res = connection.execute(db.text(query_sql))
    return res


#################################################### PATHWAYS #############################################################

def get_pathways(connection):
    query_sql = "SELECT pathways_id,from_stop_id,to_stop_id,is_bidirectional,transversal_time FROM pathways"
    res = connection.execute(db.text(query_sql))
    return res

#################################################### STOPTIMES #############################################################

def get_stop_times_matin(connection):
    query_sql = """SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence FROM stop_times WHERE departure_time < '08:00:00'"""
    tags_res_list = connection.execute(db.text(query_sql)).fetchall()
    return tags_res_list

def get_stop_times_midi(connection):
    query_sql = """SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence FROM stop_times WHERE departure_time < '16:00:00' and departure_time >= '08:00:00'"""
    tags_res_list = connection.execute(db.text(query_sql)).fetchall()
    return tags_res_list

def get_stop_times_apres_midi(connection):
    query_sql = """SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence FROM stop_times WHERE departure_time < '20:00:00' and departure_time >= '16:00:00'"""
    tags_res_list = connection.execute(db.text(query_sql)).fetchall()
    return tags_res_list

def get_stop_times_soir(connection):
    query_sql = """SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence FROM stop_times WHERE departure_time < '00:00:00' and departure_time >= '20:00:00'"""
    tags_res_list = connection.execute(db.text(query_sql)).fetchall()
    return tags_res_list

#################################################### ROUTES #############################################################

def get_routes(connection):
    query_sql = """SELECT route_id,route_short_name,route_type FROM routes"""
    tags_res_list = connection.execute(db.text(query_sql)).fetchall()
    return tags_res_list
