
"""
Method to create a dictionnary that contains data from agency.txt
[agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone]
Return a list and a dictionnary
"""
def create_dico_agency(filename): 
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is agency_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
				index += 1
			else : 
				agency_id = int(data[0])
				agency_name = data[1]
				agency_url = data[2]
				agency_timezone = data[3]
				agency_lang = data[4]
				agency_phone = data[5]
				
				dico[agency_id] = [agency_name,agency_url,agency_timezone,agency_lang,agency_phone]
		
		return format_data,dico		

"""
Method to create a dictionnary that contains data from calendar.txt
[service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date]
Return a list and a dictionnary
"""
def create_dico_calendar(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is service_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
				index += 1
			else : 
				service_id = int(data[0])
				monday = int(data[1])
				tuesday = int(data[2])
				wednesday = int(data[3])
				thursday = int(data[4])
				friday = int(data[5])
				saturday = int(data[6])
				sunday = int(data[7])
				start_date = data[8]
				end_date = data[9]
				dico[service_id] = [monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date]
		
		return format_data,dico

"""
Method to create a dictionnary that contains data from calendar_dates.txt
[service_id,date,exception_type]
Return a list and a dictionnary
"""	
def create_dico_calendar_dates(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is service_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
				index += 1
			else : 
				service_id = int(data[0])
				date = data[1]
				exception_type = int(data[2])
				dico[service_id] = [date,exception_type]
		
		return format_data,dico

"""
Method to create a dictionnary that contains data from calendar_dates.txt
[route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color]
Return a list and a dictionnary
"""		
def create_dico_routes(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is route_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
				index += 1
			else : 
				route_id = int(data[0])
				agency_id = int(data[1])
				route_short_name = data[2]
				route_long_name = data[3]
				route_desc = data[4]
				route_type = int(data[5])
				route_url = data[6]
				route_color = data[7]
				route_text_color = data[8]
				dico[route_id] = [agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color]
		
		return format_data,dico

"""
Method to create a dictionnary that contains data from stops.txt
[stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station]
Return a list and a dictionnary
"""		
def create_dico_stops(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is stop_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
				index += 1
			else : 
				stop_id = int(data[0])
				stop_code = data[1]
				stop_name = data[2]
				stop_desc = data[3]
				stop_lat = float(data[4])
				stop_lon = float(data[5])
				location_type = int(data[6])
				parent_station = data[7]
				dico[stop_id] = [stop_code,stop_name,stop_desc,stop_lat,stop_lon,location_type,parent_station]
		
		return format_data,dico

"""
Method to create a dictionnary that contains data from stop_times.txt
[trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,shape_dist_traveled]
Return a list and a dictionnary
"""		
def create_dico_stop_times(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is route_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
			else : 
				trip_id = int(data[0])
				arrival_time = data[1]
				departure_time = data[2]
				stop_id = int(data[3])
				stop_sequence = int(data[4])
				stop_headsign = data[5]
				shape_dist_traveled = data[6]
				dico[index] = [trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,shape_dist_traveled]
			
			index += 1
			
		return format_data,dico

"""
Method to create a dictionnary that contains data from transfers.txt
[from_stop_id,to_stop_id,transfer_type,min_transfer_time]
Return a list and a dictionnary
"""		
def create_dico_transfers(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is from_stop_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
				index += 1
			else : 
				from_stop_id = int(data[0])
				to_stop_id = int(data[1])
				transfer_type = int(data[2])
				min_transfer_time = int(data[3])
				dico[from_stop_id] = [to_stop_id,transfer_type,min_transfer_time]
		
		return format_data,dico

"""
Method to create a dictionnary that contains data from transfers.txt
[route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,shape_id]
Return a list and a dictionnary
"""		
def create_dico_trips(filename):
	with open(filename) as file:
		
		index = 0
		format_data = list() # store the format of the file's data
		dico = dict() # the key is route_id
		
		# get data line by line
		for line in file.readlines():
			l = line.split('\n')
			data = l[0].split(',')
			
			if index == 0: # the first line explain the format of the file
				format_data = data.copy()
			else : 
				route_id = int(data[0])
				service_id = int(data[1])
				trip_id = int(data[2])
				trip_headsign = data[3]
				trip_short_name = data[4]
				direction_id = data[5]
				shape_id = data[6]
				dico[index] = [route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,shape_id]
			
			index += 1
			
		return format_data,dico
