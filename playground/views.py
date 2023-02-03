from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .run import get_journeys, get_dict_of_stop_names, date_to_second,get_complete_name
from django.core.cache import cache

# Create your views here => REQUEST HANDLER
# takes a request -> returns a response

# def test1(request):
#     return render(request,'test.html')

def journey_view(request,source_location,destination_location,departure_time,arrival_time):
    # journeys = [
    # {
    #     'departure_time': "08:12:11",
    #     'duration_time' : "00:20:00",
    #     'arrival_time': '07:00:11',
    #     'journey': [
    #         {'transport_mode': 'Ligne/RER-B', 'destination_name': 'Gare du Nord'},
    #         {'transport_mode': 'Ligne/RER-B', 'destination_name': 'Châtelet les Halles'},
    #         {'transport_mode': 'Ligne/RER-B', 'destination_name': 'Saint-Michel Notre-Dame'},
    #         {'transport_mode': 'Ligne/RER-B', 'destination_name': 'Luxembourg'},
    #         {'transport_mode': None, 'destination_name': 'Luxembourg'},
    #         {'transport_mode': 'Bus-89', 'destination_name': 'Luxembourg'},
    #         {'transport_mode': 'Bus-89', 'destination_name': 'Panthéon'},
    #         {'transport_mode': 'Bus-89', 'destination_name': 'Lycée Henri IV'},
    #         {'transport_mode': 'Bus-89', 'destination_name': 'Cardinal Lemoine - Monge'},
    #         {'transport_mode':  None, 'destination_name': 'Jussieu'},
    #     ]
    # }]

    journeys = get_journeys(source_location,destination_location,departure_time, arrival_time)
    journeys_sorted_by_duration = sorted(journeys, key=lambda x: date_to_second(x["duration_time"]))
    return render(request, 'itinerary.html', {'journeys': journeys_sorted_by_duration})




def landing_page(request):
    if request.method == 'POST':
        source_location = request.POST.get('source_location')
        destination_location = request.POST.get('destination_location')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        
        location_to_IFDM = get_location_to_IFDM_dict()
        source_location = location_to_IFDM[source_location]
        destination_location = location_to_IFDM[destination_location]
        # Departure At Feature -> user input the departure time but not the arrival time
        # Arrival at feature -> USer input the arrival time only, or both the arrvial time and departure  time
        #Note :  time is taken as HHMM but needed as HHMMSS
        
        # Departure at feature : 
        if departure_time != "" and arrival_time == "":
            departure_time +=":00" 
            arrival_time = "23:59:59"
            # Journeys = get_journeys(source_location,destination_location,departure_time)
            return journey_view(request, source_location,destination_location,departure_time,arrival_time)
        
        # Arrival at feature: 
        elif arrival_time != "" and departure_time == '' :
            departure_time = "00:00:00" 
            arrival_time += ":00"
            return journey_view(request, source_location,destination_location,departure_time,arrival_time)


        elif arrival_time != "" and departure_time != '':
            departure_time +=":00"
            arrival_time += ":00"
            if date_to_second(departure_time) >= date_to_second(arrival_time) :
                error_message = "Arrival time must be after departure time."
                locations = cache.get("locations")
                form = SearchForm()
                return render(request, 'landing_page.html', {'form': form, "locations": locations,'error_message': error_message})
            return journey_view(request, source_location,destination_location,departure_time,arrival_time)

            
    else:
        form = SearchForm()
        
        # locations = ["location1","location2 "]
        # cache.set('locations', locations, 3600)
        
        locations = cache.get('locations')
        if not locations:
            locations = sorted(list(get_dict_of_stop_names().values()))
            cache.set('locations', locations, 3600) # cache for 1 hour
        
        
        return render(request, 'landing_page.html', {'form': form, "locations": locations})
    
def get_location_to_IFDM_dict():
    location_to_IFDM= cache.get("location_to_IFDM")
    if location_to_IFDM: 
        return location_to_IFDM
    
    IFDM_to_location = get_dict_of_stop_names()
    location_to_IFDM = {}
    for key, value in IFDM_to_location.items():
        location_to_IFDM[value] = key
    cache.set('location_to_IFDM',location_to_IFDM, 3600)
    return location_to_IFDM