import sys
import sqlalchemy as db
import request_db as rdb
import time
import re


############################# UTILS FUNCTIONS ########################################

"""
Method to transform the string "hh:mm:ss" into the number of seconds corresponding 
Return a int
"""
def date_to_second(date_time):
	time_re = re.compile(r"(\d+):(\d+):(\d+)")
	hour,minute,second = time_re.match(date_time).groups()
	return int(hour)*3600 + int(minute)*60 + int(second)

"""
Method to check if each footpath contains a self loop
"""
def percent_self_loop(footpaths):
	number_footpaths = 0
	number_selfloop = 0

	for k,v in footpaths.items():
		for ele in v :
			if k == ele[0]:
				number_selfloop += 1

		number_footpaths += 1

	print("number of footpaths : " + str(number_footpaths))
	print("number of self loop : " + str(number_selfloop))

"""
Method to transform a number of seconds into a time:string --> "hh:mm:ss"
Return a string
"""
def second_to_date(second_time):
	hours = second_time // 3600
	time_restant = second_time % 3600
	minutes = time_restant // 60
	seconds = time_restant % 60

	hh = str(hours)
	mm = str(minutes)
	ss = str(seconds)
	
	if hours < 10: hh = "0" + str(hours) 
	if minutes < 10: mm = "0" + str(minutes)
	if seconds < 10: ss = "0" + str(seconds)

	res = hh + ":" + mm + ":" + ss
	return res

"""
Method to get informations on the route used
Return a string
"""
def get_informations_route(route_id,routes): 

	data = routes[route_id]
	route_name = data[0]
	route_type = data[1]

	res = ""
	if route_type == 0: 
		res = "Tram"
	elif route_type == 1:
		res = "M"
	elif route_type == 2:
		res = "Ligne/RER"
	elif route_type == 3:
		res = "Bus"
	elif route_type == 7:
		res = "Furniculaire"
	else:
		res = "Autre"
	
	return res + "-" + route_name

############################# GET DATA FROM REQUESTS SQL ########################################

def find_stop(stop_name):
	engine,connection,metadata = rdb.connection_database()
	res = rdb.search_stop(stop_name,connection)
	return res

def create_timetable():
	
	start_time = time.time()
	stops = get_stops()
	print("--- %s seconds get_stop---" % (time.time() - start_time))

	start_time = time.time()
	trips = get_trips()
	print("--- %s seconds get_trips---" % (time.time() - start_time))

	start_time = time.time()
	footpaths = get_footpaths(stops)
	print("--- %s seconds get_footpaths---" % (time.time() - start_time))

	start_time = time.time()
	connections = get_connections()
	print(len(connections))
	print("--- %s seconds get_connections---" % (time.time() - start_time))

	return (stops,connections,trips,footpaths)

"""
Method to get the stops from the database
Return a dictionnary --> [stop_id] = stop_name
"""
def get_stops():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_stops(connection)
	stops = dict()	

	for ele in res:
		stop_id = ele[0]
		stop_name = ele[1]
		
		if stop_id not in stops:
			stops[stop_id] = stop_name
		else:
			print(stop_id)
	return stops

"""
Method to get the trips from the database
Return a dictionnary --> [trip_id] = (trip_name,route_id)
"""
def get_trips():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_trips(connection)
	trips = dict()

	for ele in res:
		trip_id = ele[0]
		trip_name = ele[1]
		route_id = ele[2]
		
		if trip_id not in trips:
			trips[trip_id] = (trip_name,route_id)
		else:
			print(trip_id)
	return trips

"""
Method to get the transfers from the database
Return a dictionnary --> [from_stop_id] = [(to_stop_id,time_length)]
"""
def get_transfers():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_transfers(connection)
	transfers = dict()

	for ele in res:
		from_stop_id = ele[0]
		to_stop_id = ele[1]
		time_length = int(ele[3])		

		if from_stop_id not in transfers:
			transfers[from_stop_id] = [(to_stop_id,time_length)]
		else:
			transfers[from_stop_id].append((to_stop_id,time_length))

	return transfers

"""
Method to get the pathways from the database
Return a dictionnary --> [from_stop_id] = [(to_stop_id,time_length)]
"""
def get_pathways():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_pathways(connection)
	pathways = dict()

	for ele in res:
		from_stop_id = ele[1]
		to_stop_id = ele[2]
		is_bi = int(ele[3])
		transversal_time = int(ele[4])
		
		"""
		if is_bi == 0:
			print(pathways_id)		
		"""
		
		if from_stop_id not in pathways:
			pathways[from_stop_id] = [(to_stop_id,transversal_time)]
		else:
			pathways[from_stop_id].append((to_stop_id,transversal_time))

	return pathways

"""
Method to get the footpaths from transfers and pathways
Return a dictionnary --> [from_stop_id] = [(to_stop_id,time_length)]
"""
def get_footpaths(stops): 
	transfers = get_transfers()
	pathways = get_pathways()
	footpaths = dict()

	# TRANSFERS
	for k,v in transfers.items():
		if k not in footpaths:
			footpaths[k] = v
		else:
			for ele in v:
				footpaths[k].append(ele)	
	
	# PATHWAYS
	for k,v in pathways.items():
		if k not in footpaths:
			footpaths[k] = v
		else:
			for ele in v:
				footpaths[k].append(ele)	
	
	# ADDING SELF LOOP --> obligation pour respecter scan 
	for k in stops.keys():
		self_loop = (k,0)

		if k not in footpaths:
			footpaths[k] = [self_loop]
		else:
			footpaths[k].append(self_loop)	

	return footpaths

def get_stop_times_matin():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_stop_times_matin(connection)
	stop_times = dict()   

	for ele in res:

		trip_id = ele[0]
		arrival_time = ele[1]
		depart_time = ele[2]
		stop_id = ele[3]
		stop_sequence = int(ele[4])
		
		if trip_id not in stop_times:
			stop_times[trip_id] = [(arrival_time,depart_time,stop_id,stop_sequence)]
		else:
			stop_times[trip_id].append((arrival_time,depart_time,stop_id,stop_sequence))

	return stop_times

def get_stop_times_midi():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_stop_times_midi(connection)
	stop_times = dict()

	for ele in res:

		trip_id = ele[0]
		arrival_time = ele[1]
		depart_time = ele[2]
		stop_id = ele[3]
		stop_sequence = int(ele[4])
		
		if trip_id not in stop_times:
			stop_times[trip_id] = [(arrival_time,depart_time,stop_id,stop_sequence)]
		else:
			stop_times[trip_id].append((arrival_time,depart_time,stop_id,stop_sequence))

	return stop_times

def get_stop_times_apres_midi():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_stop_times_apres_midi(connection)
	stop_times = dict()

	for ele in res:

		trip_id = ele[0]
		arrival_time = ele[1]
		depart_time = ele[2]
		stop_id = ele[3]
		stop_sequence = int(ele[4])
		
		if trip_id not in stop_times:
			stop_times[trip_id] = [(arrival_time,depart_time,stop_id,stop_sequence)]
		else:
			stop_times[trip_id].append((arrival_time,depart_time,stop_id,stop_sequence))

	return stop_times

def get_stop_times_soir():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_stop_times_soir(connection)
	stop_times = dict()

	for ele in res:

		trip_id = ele[0]
		arrival_time = ele[1]
		depart_time = ele[2]
		stop_id = ele[3]
		stop_sequence = int(ele[4])
		
		if trip_id not in stop_times:
			stop_times[trip_id] = [(arrival_time,depart_time,stop_id,stop_sequence)]
		else:
			stop_times[trip_id].append((arrival_time,depart_time,stop_id,stop_sequence))

	return stop_times


def get_connections():
	
	start_time = time.time()
	st_matin = get_stop_times_matin()
	print("--- %s seconds get_stop_times_matin---" % (time.time() - start_time))
	"""
	start_time = time.time()
	st_midi = get_stop_times_midi()
	print("--- %s seconds get_stop_times_midi---" % (time.time() - start_time))

	start_time = time.time()
	st_apres_midi = get_stop_times_apres_midi()
	print("--- %s seconds get_stop_times_apres_midi---" % (time.time() - start_time))

	start_time = time.time()
	st_soir = get_stop_times_soir()
	print("--- %s seconds get_stop_times_soir---" % (time.time() - start_time))
	"""
	################################# MANAGE CONNECTIONS BY TRIPS ######################################
	
	connections = dict()

	# CONNECTIONS MATIN
	for k,v in st_matin.items():

		if k not in connections:
			connections[k] = v.copy()
		else:
			for ele in v:
				connections[k].append(ele)
	"""
	# CONNECTIONS MIDI
	for k,v in st_midi.items():

		if k not in connections:
			connections[k] = v.copy()
		else:
			for ele in v:
				connections[k].append(ele)

	# CONNECTIONS APRES-MIDI
	for k,v in st_apres_midi.items():

		if k not in connections:
			connections[k] = v.copy()
		else:
			for ele in v:
				connections[k].append(ele)

	# CONNECTIONS SOIR
	for k,v in st_soir.items():

		if k not in connections:
			connections[k] = v.copy()
		else:
			for ele in v:
				connections[k].append(ele)
	"""

	################################# MANAGE CONNECTIONS FORMATED ######################################

	# Rappel : connections = [trip_id] = [((arrival_time,depart_time,stop_id,stop_sequence))]

	connections_formatted = list()

	for k,v in connections.items():

		trip_id = k
		con = sorted(v, key=lambda x: x[3]) # sort connection for this trip_id by stop_sequence
		
		for i in range(len(con)-1):
			dep_time = date_to_second(str(con[i][1]))
			arr_time = date_to_second(str(con[i+1][0]))
			dep_stop = con[i][2]
			arr_stop = con[i+1][2]
			connection = (dep_stop,arr_stop,dep_time,arr_time,trip_id)
			connections_formatted.append(connection)

	################################# MANAGE CONNECTIONS SORTED ######################################

	connections_sorted = sorted(connections_formatted,key=lambda x:x[2])
	return connections_sorted

"""
Method to get the routes from the database
Return a dictionnary --> [route_id] = (route_name,route_type)
"""
def get_routes():
	engine,connection,metadata = rdb.connection_database()
	res = rdb.get_routes(connection)
	routes = dict()	

	for ele in res:
		route_id = ele[0]
		route_name = ele[1]
		route_type = int(ele[2])

		if route_id not in routes:
			routes[route_id] = (route_name,route_type)
		else:
			print(route_id)
	return routes


#################################### CONNECTION SCAN ALGORITHM ##########################################

"""
Informations : 
	timetable : (stops,connections,trips,footpaths)
	stops : [stop_id] = stop_name
	connections :  [(dep_stop,arr_stop,dep_time,arr_time,trip_id)]
	trips : [trip_id] = (trip_name,route_id) 
	footpaths : [from_stop_id] = [(to_stop_id,transversal_time)] 
"""
def connection_scan_algorithm(timetable,source,target,source_time):

	print("The source is : " + source)
	print("The destination is : " + target)
	print("The depart time is : " + str(source_time) + " ---> " + second_to_date(source_time))

	S = dict()
	T = dict()
	J = dict()
	
	# INITIALIZATION	
	for stop in timetable[0].keys():
		S[stop] = float('inf')
		J[stop] = (None,None,None)

	for trip in timetable[2].keys():
		T[trip] = None

	for footpath in timetable[3][source]:
		destination = footpath[0]
		duration = footpath[1]
		S[destination] = source_time + duration
	
	# MAIN LOOP	
	for c in timetable[1]:

		c_dep_stop = c[0]
		c_arr_stop = c[1]
		c_dep_time = c[2]
		c_arr_time = c[3]
		c_trip = c[4]

		if T[c_trip] is not None or S[c_dep_stop] <= c_dep_time:
			
			if T[c_trip] is None: 
				T[c_trip] = c
			
			for f in timetable[3][c_arr_stop]:

				f_arr_stop = f[0]
				f_dur = f[1]

				if c_arr_time + f_dur < S[f_arr_stop]:
					S[f_arr_stop] = c_arr_time + f_dur
					J[f_arr_stop] = (T[c_trip],c,f)

	# EXTRACT JOURNEY
	journey = list()
	t = target

	while J[t] != (None,None,None):
		journey.append(J[t])
		t = J[t][1][0]

	return journey


#################################### CONNECTION SCAN ALGORITHM VARIANTE ##########################################

"""
Informations : 
	timetable : (stops,connections,trips,footpaths)
	stops : [stop_id] = stop_name
	connections :  [(dep_stop,arr_stop,dep_time,arr_time,trip_id)]
	trips : [trip_id] = (trip_name,route_id) 
	footpaths : [from_stop_id] = [(to_stop_id,transversal_time)] 
"""
def connection_scan_algorithm_multires(timetable,source,target,source_time,number_res):

	print("The source is : " + source)
	print("The destination is : " + target)
	print("The depart time is : " + str(source_time) + " ---> " + second_to_date(source_time))

	S = dict()
	T = dict()
	J = dict()

	trips_forbiden = set()
	res = list()

	while len(res) <= number_res:
	
		# INITIALIZATION	
		for stop in timetable[0].keys():
			S[stop] = float('inf')
			J[stop] = (None,None,None)

		for trip in timetable[2].keys():
			T[trip] = None

		for footpath in timetable[3][source]:
			destination = footpath[0]
			duration = footpath[1]
			S[destination] = source_time + duration
		
		# MAIN LOOP	
		for c in timetable[1]:

			c_dep_stop = c[0]
			c_arr_stop = c[1]
			c_dep_time = c[2]
			c_arr_time = c[3]
			c_trip = c[4]

			route_id = timetable[2][c_trip][1]

			# avoid trips already use 
			if route_id not in trips_forbiden:

				if T[c_trip] is not None or S[c_dep_stop] <= c_dep_time:
					
					if T[c_trip] is None: 
						T[c_trip] = c
					
					for f in timetable[3][c_arr_stop]:

						f_arr_stop = f[0]
						f_dur = f[1]

						if c_arr_time + f_dur < S[f_arr_stop]:
							S[f_arr_stop] = c_arr_time + f_dur
							J[f_arr_stop] = (T[c_trip],c,f)

		# EXTRACT JOURNEY
		journey = list()
		t = target

		while J[t] != (None,None,None):
			journey.append(J[t])
			t = J[t][1][0]

		res.append(journey.copy())

		# UPDATE TRIPS FORBIDEN
		for ele in journey:
			route_id = timetable[2][ele[1][4]][1]
			#route_name = routes[route_id][0]
			
			#trip_id = ele[1][4]
			if route_id not in trips_forbiden:
				trips_forbiden.add(route_id)
				break

	return res


#################################### ANALYSE JOURNEY ##########################################
	
def analyse_journey(journey,stops,trips,routes):

	print("--------------------------------")
	print("-          JOURNEY             -")
	print("--------------------------------")

	journey.reverse()
	
	for i in range(len(journey)):
		c = journey[i][1]
		f = journey[i][2]

		trip_name = trips[c[4]][0]
		route_id = trips[c[4]][1]
		dep_time = c[2]
		arr_time = c[3]

		data_route = get_informations_route(route_id,routes)

		print(c[4] + " :: " + data_route + " ["+ trip_name + "] : " + stops[c[0]])
		if f[1] != 0:
			print(c[4] + " :: " + data_route + " ["+ trip_name + "] : " + stops[c[1]] + ' ( '  +' --> ' + second_to_date(arr_time) + ')')
			print("---------------------------------")
			print("walk to : " + stops[f[0]] + " (" + str(f[1]) + ")")
			print("---------------------------------")

		
		if i == len(journey)-1 and f[1] == 0:
			print(c[4] + " :: " + data_route + " ["+ trip_name + "] : " + stops[c[1]] + ' (arr :' + second_to_date(arr_time) + ')')


def analyse_journey_compacte(journey,stops,trips,routes):

	print("--------------------------------------------------------------------------")

	#journey.reverse()
	new_trajet = True
	for i in range(len(journey)):
		c = journey[i][1]
		f = journey[i][2]

		trip_name = trips[c[4]][0]
		route_id = trips[c[4]][1]
		dep_time = c[2]
		arr_time = c[3]

		data_route = get_informations_route(route_id,routes)

		

		# pas de changement AND nouveau trajet
		if f[1] == 0 and new_trajet == True:
			print(data_route + " ["+ trip_name + "] : (" + second_to_date(dep_time) + ") " 
				+ stops[c[0]] + " --> ", end='')
			new_trajet = False

		# pas de changement AND pas nouveau trajet
		elif f[1] == 0 and new_trajet == False and i != len(journey)-1:
			continue
		
		# changement AND nouveau trajet
		elif f[1] != 0 and new_trajet == True:
			print(data_route + " ["+ trip_name + "] : (" + second_to_date(dep_time) + ") " 
				+ stops[c[0]] + " --> " + stops[c[1]] + " (" + second_to_date(arr_time) + ")")
			print("walk to : " + stops[f[0]] + " (" + str(f[1]) + ")")
			new_trajet = False

		# changement AND pas nouveau trajet
		else:	
			print(stops[c[1]] + " (" + second_to_date(arr_time) + ")")
			print("walk to : " + stops[f[0]] + " (" + str(f[1]) + ")")
			new_trajet = True
		
#################################### MAIN ##########################################	

def main():

	routes = get_routes()

	timetable = create_timetable()
	source = "IDFM:22007"
	target = "IDFM:21968"
	source_time = date_to_second('06:50:00')

	journeys = connection_scan_algorithm_multires(timetable,source,target,source_time,5)
	
	for j in journeys:
		analyse_journey(j,timetable[0],timetable[2],routes)

	for j in journeys:
		analyse_journey_compacte(j,timetable[0],timetable[2],routes)

if __name__ == "__main__":
    # execute only if run as a script
    main()

