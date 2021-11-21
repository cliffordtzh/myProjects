# Import external packages
import numpy as np
from tqdm import trange

# Import local classes and functions
from classes.classes import *
from functions.functions import *


def main():
    '''
    Simulation of M/M/1 queue system. 2 Offices in California are used, Blythe and 29 Palms office. 

    LAMBDA values are approximated from data from June California DMV data.
    https://www.dmv.ca.gov/portal/file/june_2021_wait_times-pdf/

    MU values are approximated from 
    https://www.shmula.com/dmv-test-waiting-line-at-department-of-motor-vehicles/10632/

    Long run waiting time (LRWq) values are calculated from the M/M/1 formula for long run waiting time.
        LRWq = LAMBDA/(MU*(MU - LAMBDA))

    Time intervals are in increments of 0.1min, with all time related values (Service time and Interarrival Time) rounded to 0.1min

    Customer interarrivals are exponentially distributed with a mean of LAMBDA
    Service times are exponentially distributed with a mean of MU
    
    First arrival time is initialised to np.random.exponential(LAMBDA)
    When the interarrival time is reached, the queue pulls the customer into the system, and the customer's system_in and queue_in attributes
    are updated to current time. The next arrival time is calculated
        next arrival time = current time + interarrival time

    If the queue is not empty, and the server is idle, the queue pushes the customer to the server. The queue_out time is updated to the current time
    The service time is calculated and passed into the queue object, which passes it to its server and stored. When the service time is reached,
    the customer is ejected from the system, and the system_out time is updated to current time.

    At every time interval, queue and servers' time attributes are updated to current time. The queue object will try to push customers and checks if
    the next arrival time is reached. Servers will check if the service time has been reached.

    Whenever a customer is ejected, the waiting time and sojourn time is calculated
        waiting time = queue_out - queue_in
        sojourn time = sys_out - sys_in

    Each time a customer exits the system, the waiting time is averaged to show the behavior of long run average waiting time.
    This is then plotted against time to show the effects of long run on waiting times.

    The number of intervals ran is 100,000, and each interval is 0.1s of simulation time. Hence a total of 10,000 minutes, or approximately 1 week.
    We find that for Blythe, a long run of 1 week is sufficient for the waiting times to converge, while for 29 Palms, a longer time may be needed.
    '''

    time = 0
    limit = 100000
    iterations_ran = 0

    office = int(input("Select an office to simulate: "))
    LAMBDA, MU, S, LRWq, office = get_var(office)
    
    queue = Queue(0, MU)
    server = queue.server
    waiting_times = []
    sojourn_times = []

    next_arrival_time = round(time + np.random.exponential(LAMBDA), 1)

    with trange(limit) as tbar:
        while iterations_ran < limit:
            queue.update(time)
            served = server.update(time)
            if isinstance(served, Customer):
                served.sys_out = time
                waiting_times.append(served.queue_out - served.queue_in)
                sojourn_times.append(served.sys_out - served.sys_in)

            service_time = round(time + np.random.exponential(queue.server.MU), 1)
            queue.push(service_time, time)

            pulled = queue.pull(next_arrival_time)
            if pulled:
                next_arrival_time = round(time + np.random.exponential(LAMBDA), 1)

            time += 0.1
            iterations_ran += 1
            tbar.update(1)

    simulation_results(queue, server, sojourn_times, waiting_times, time, S)

    return sojourn_times, waiting_times, time, LRWq, office

if __name__ == '__main__':
    st, wt, sim_time, LRWq, office = main()
    plot_results(st, wt, sim_time, LRWq, office)
    