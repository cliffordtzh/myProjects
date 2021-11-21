import numpy as np
import pandas as pd
from tqdm import trange
import seaborn as sns
import matplotlib.pyplot as plt


def sim_MM1(office):
    """
    simulating S number of M/M/1 queue
    """

    if office == 0:
        LAMBDA = 1/0.182
        MU = 1/0.420
        S = 1
        LRWq = 1.821
        office = 'Blythe'

    elif office == 1:
        LAMBDA = 1/0.378
        MU = 1/0.420
        S = 1
        LRWq = 21.429
        office = '29 Palms'

    elif office == 2:
        LAMBDA = 1/0.560
        MU = 1/0.420
        S = 2
        LRWq = 4.762
        office = 'Brawley'

    class Customer():
            def __init__(self):
                self.sys_in = 0
                self.sys_out = 0
                self.queue_in = 0
                self.queue_out = 0

    class Server():
        def __init__(self, num):
            self.name = num
            self.served = 0
            self.idle = True
            self.service_time = 0
            self.serving = None

        def serve(self, customer):
            self.idle = False
            self.service_time = round(np.random.exponential(MU) + time, 1)
            self.serving = customer

        def update(self):
            if self.idle == False:
                if time >= self.service_time:
                    self.served += 1
                    self.idle = True
                    self.service_time = 0
                    self.serving.sys_out = time
                    sojourn_times.append(self.serving.sys_out - self.serving.sys_in)
                    del self.serving; self.serving = None

    class Queue(list):
        def __init__(self, num):
            self.name = num
            self.server = Server(num)

        def pull(self, next_arrival_time):
            if time > next_arrival_time:
                customer = Customer()
                self.append(customer)
                customer.sys_in = time
                customer.queue_in = time
                return True
            return False

        def push(self):
            for server in servers:
                if server.idle == True and len(self) > 0:
                    customer = self.pop(0)
                    server.serve(customer)
                    customer.queue_out = time
                    waiting_times.append(customer.queue_out - customer.queue_in)

    limit = 100000
    iterations_ran = 0
    sim_time = 600
    turn = 0
    time = 0
    next_arrival_time = np.random.exponential(LAMBDA)

    queue = [Queue(i) for i in range(S)]
    servers = [queue[i].server for i in range(S)]
    sojourn_times = []
    waiting_times = []

    def generate_arrival(arrival_time):
        arrival = np.random.exponential(LAMBDA)
        arrival_time += arrival

        return arrival_time

    with trange(limit) as tbar:
        while iterations_ran < limit:
            if turn == S:
                turn = 0

            for i in range(S):
                if i == turn:
                    pulled = queue[i].pull(next_arrival_time)
                    if pulled:
                        next_arrival_time = generate_arrival(next_arrival_time)
                        turn += 1
                queue[i].push()
                servers[i].update()

            time += 0.1
            time = round(time, 1)
            iterations_ran += 1
            tbar.update(1)

    for i in range(S):
        q = queue[i]
        s = servers[i]

        print(f"Queue {q.name} Length: {len(q)}")
        print(f"Server {s.name} served {s.served} customers")
        print(f"Server {s.name} is idle {s.idle}")
    
    total_served = sum([s.served for s in servers])

    print(f"------------------------ Total Time Ran: {time:.3f} minutes ----------------------")
    print(f"Average Sojourn Time: {np.mean(sojourn_times):.3f} minutes")
    print(f"Average Waiting Time: {np.mean(waiting_times):.3f} minutes")
    print(f"Total customers served: {total_served}")

    return sojourn_times, waiting_times, total_served, time, LRWq, office



if __name__ == '__main__':
    # To run the simulation, change office to either 0, 1 or 2 to represent Blythe, 29 Palms or Brawley
    office = 0
    st, wt, ts, sim_time, LRWq, office = sim_MM1(office)

    average_waiting_times = [np.average(wt[0:i+1]) for i in range(len(wt))]
    sns.lineplot(x = np.linspace(0, sim_time, len(average_waiting_times)), y = average_waiting_times)
    plt.hlines(LRWq, 0, sim_time, label = 'Long Run Wq', color = 'red')
    plt.scatter(x = 600, y = LRWq, label = "Closing time for {office}", color = 'green', s = 20)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Average Waiting Times, Wq (minutes)")
    plt.title(f"Simulating {office} to Infinity. Minutes elapsed: {sim_time:.2f}")
    plt.legend()
    plt.show()