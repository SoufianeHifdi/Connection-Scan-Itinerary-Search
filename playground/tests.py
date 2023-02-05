from django.test import TestCase
from . import run as rn
from . import utils as utl
import time
import matplotlib.pyplot as plt

# Create your tests here.
class perfTest(TestCase):
    def test(self):
        routes = utl.get_routes()
        timetable = utl.create_timetable()
        source = "IDFM:22007"
        target = "IDFM:21968"
        source_time = utl.date_to_second('06:00:00')


        target_time = list()
        target_time.append(utl.date_to_second('06:30:00'))
        target_time.append(utl.date_to_second('07:00:00'))
        target_time.append(utl.date_to_second('07:30:00'))
        target_time.append(utl.date_to_second('08:00:00'))
        target_time.append(utl.date_to_second('08:30:00'))
        target_time.append(utl.date_to_second('09:00:00'))
        target_time.append(utl.date_to_second('09:30:00'))
        target_time.append(utl.date_to_second('10:00:00'))
        # target_time.append(utl.date_to_second('11:00:00'))
        # target_time.append(utl.date_to_second('12:00:00'))
        # target_time.append(utl.date_to_second('13:00:00'))
        # target_time.append(utl.date_to_second('14:00:00'))
        # target_time.append(utl.date_to_second('15:00:00'))
        # target_time.append(utl.date_to_second('16:00:00'))
        # target_time.append(utl.date_to_second('17:00:00'))
        # target_time.append(utl.date_to_second('18:00:00'))
        # target_time.append(utl.date_to_second('19:00:00'))
        
        intervals = []
        journeys = []
        times = []
        interval = 0.5#hour
        for ele in target_time:
            start_time = time.time()
            RES = rn.connection_scan_algorithm_multires(timetable,source,target,source_time,ele,10000)
            # print("--- %s seconds get_stop---" % (time.time() - start_time))
            # print(type((time.time() - start_time)))
            times.append((time.time() - start_time))
            journeys.append(len(RES))
            intervals.append(interval)
            interval +=0.5
            # print("number of journeys : " + str(len(RES)))

        # plt.plot(intervals, journeys)
        # plt.xlabel("Time Interval")
        # plt.ylabel("Number of Journeys")
        # plt.show()
        # plt.savefig("journey_plot.png")
            # print(times,journeys,intervals)
            fig, ax1 = plt.subplots()

            color = 'tab:red'
            ax1.set_xlabel('Time Interval')
            ax1.set_ylabel('Number of Journeys', color=color)
            ax1.plot(intervals, journeys, color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx() 

            color = 'tab:blue'
            ax2.set_ylabel('Execution Time (Seconds)', color=color)  
            ax2.plot(intervals, times, color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()  
            plt.savefig("journey_plot"+str(interval)+".png")
            plt.show()  
            # plt.savefig("journey_plot"+interval+".png")