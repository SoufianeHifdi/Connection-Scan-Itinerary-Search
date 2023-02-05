from . import request_db as rdb
from . import utils as utl
from django.core.cache import cache

#################################### CONNECTION SCAN ALGORITHM VARIANTE ##########################################

"""
Informations : 
	timetable : (stops,connections,trips,footpaths)
	stops : [stop_id] = stop_name
	connections :  [(dep_stop,arr_stop,dep_time,arr_time,trip_id)]
	trips : [trip_id] = (trip_name,route_id) 
	footpaths : [from_stop_id] = [(to_stop_id,transversal_time)] 
"""
def connection_scan_algorithm_multires(timetable,source,target,source_time,target_time,number_res):

	print("The source is : " + source)
	print("The destination is : " + target)
	print("The depart time is : " + str(source_time) + " ---> " + utl.second_to_date(source_time))

	# PREPROCESSING
	S = dict()
	T = dict()
	J = dict()

	connection_forbiden = set()
	res = list()

	# lOOP
	while len(res) < number_res:
	
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

			# optimisation 
			if c_dep_time > target_time:
				break

			tmp = (c_dep_stop,c_arr_stop,c_dep_time,c_arr_time)

			# avoid trips already use 
			if tmp not in connection_forbiden:

				if S[c_dep_stop] <= c_dep_time:
					
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
		counter_security = 0
		t_seen = set()

		while J[t] != (None,None,None) and counter_security < 200:
			t_seen.add(t)
			journey.append(J[t])
			
			t1 = J[t][1][0]
			if t1 in t_seen: 
				t = J[t][0][0]
			else:
				t = t1
			counter_security += 1

		# loop detected
		if counter_security >= 200:
			print("skipped - loop detected")
			journey.reverse()
			print(journey)
			return res

		# adding the first footpath --> footpath of the source
		for f in timetable[3][source]:
			if f[0] == t:
				print("done")
				journey.append((None,None,f))

		journey.reverse()
		
		# any solution found
		if len(journey) == 0 :
			print("no more journeys")
			return res

		arrival_time = utl.compute_arrival_time(journey)
		print(utl.second_to_date(arrival_time))

		# if the journey computed does not respect the target time --> no more solution
		if arrival_time > target_time:
			return res
		
		else:

			res.append(journey.copy())

			# UPDATE TRIPS FORBIDEN
			for ele in journey:
				c = ele[1]

				if c is not None:
					tmp = (c[0],c[1],c[2],c[3])
				
					if tmp not in connection_forbiden:
						connection_forbiden.add(tmp)
						break
	
	print("limit reached")
	return res

###################################### MANAGE JOURNEY ##############################

def  get_path_journey(journey,stops,trips,routes):
	res = list()

	for ele in journey:
		c = ele[1]
		f = ele[2]

		# only a footpath to another station
		if c is None and f[1] != 0:
			d = dict()
			d["transport_mode"] = None
			d["destination_name"] = stops[f[0]]
			res.append(d)

		# a connection
		if c is not None: 
			trip_name = trips[c[4]][0]
			route_id = trips[c[4]][1]
			data_route = utl.get_informations_route(route_id,routes)
			
			d = dict()
			d["transport_mode"] = data_route + " ["+ trip_name + "]"
			d["destination_name"] = stops[c[0]]
			res.append(d)

			# a connection with a footpath to another station
			if f[1] != 0:
				d = dict()
				d["transport_mode"] = data_route + " ["+ trip_name + "]"
				d["destination_name"] = stops[c[1]]
				res.append(d)
				
				d = dict()
				d["transport_mode"] = None
				d["destination_name"] = stops[f[0]]
				res.append(d)

	return res

"""
Method to create a structure of a journey --> for the fronted
"""
def create_journey_data(journey,stops,trips,routes,source):
	res = dict()

	departure_time = utl.compute_departure_time(journey)
	arrival_time = utl.compute_arrival_time(journey)
	duration_time = arrival_time - departure_time

	j = get_path_journey(journey,stops,trips,routes)

	res["source"] = stops[source]
	res["duration_time"] = utl.second_to_date(duration_time)
	res["departure_time"] = utl.second_to_date(departure_time)
	res["arrival_time"] = utl.second_to_date(arrival_time)
	res["journey"] = j.copy()

	return res

"""
Method to create a list of structure which contains all journeys --> for the frontend
"""
def create_journeys(output,stops,trips,routes,source):
	journeys = list()

	for ele in output:
		d = create_journey_data(ele,stops,trips,routes,source)
		journeys.append(d)

	return journeys


def get_journeys(source_location,destination_location,target_departure_time, target_arrival_time):
	NB_JOURNEYS = 50
	timetable = tuple()
	routes = list()
	
	if cache.get('timetable') is None :  
		timetable = utl.create_timetable()
		cache.set("timetable",timetable, 3600)
	else :
		timetable = cache.get("timetable")
	
	if len(routes) == 0:
		routes = utl.get_routes()
		cache.set("routes", routes, 3600)
	else :
		cache.get("routes")
	
	output = connection_scan_algorithm_multires(timetable,source_location,destination_location,utl.date_to_second(target_departure_time),utl.date_to_second(target_arrival_time)	,NB_JOURNEYS)
	journeys = create_journeys(output,timetable[0],timetable[2],routes,source_location)
	
	
	# for j in journeys:
	# 	journey_dict = analyse_journey(j,timetable[0],timetable[2],routes)
	# 	list_of_journeys.append(journey_dict) # TODO doit sortir un dictionnaire par trajet
	
	return journeys


#TODO MAYBE RENAME THIS METHOD --> create cache ??
def get_dict_of_stop_names():
	stops_name_dict = cache.get('stops_name_dict')
	if stops_name_dict : 
		return stops_name_dict
	
	timetable = tuple()
	routes = list()
	
	if cache.get('timetable') is None :  
		timetable = utl.create_timetable()
		cache.set("timetable",timetable, 3600)
	else :
		timetable = cache.get("timetable")
	
	if len(routes) == 0:
		routes = utl.get_routes()
		cache.set("routes", routes, 3600)
	else :
		cache.get("routes")
	
	stops_name_dict = utl.get_complete_name(timetable[0],timetable[1],timetable[2],routes)
	cache.set('stops_name_dict',stops_name_dict, 3600)
	return stops_name_dict


