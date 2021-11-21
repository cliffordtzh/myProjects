"""
classes defined for the simulation
Customer: Holds the values needed to calculate sojourn and waiting time
Server: Defines the functions needed to serve a customer, and counts the total number of customers served
Queue: Object to store customers in line, pushes customers to the server, pulls customers once the last one has arrived

Customers are generated within the queue object when the time is reached
Servers are stored in the queue object, since queues and servers are in the same system for M/M/1 queue
Queues are basically lists, with additional functions to pull and push
"""

class Customer:
    def __init__(self):
        self.queue_in = 0
        self.queue_out = 0
        self.sys_in = 0
        self.sys_out = 0


class Server:
    def __init__(self, num, MU):
        self.name = num
        self.served = 0
        self.service_time = None
        self.idle = True
        self.serving = None
        self.MU = MU
        self.time = 0

    def serve(self, customer, service_time):
        self.idle = False
        self.serving = customer
        self.service_time = service_time

    def update(self, time):
        self.time = round(time, 1)
        if self.idle == False and time > self.service_time:
            self.served += 1
            self.service_time = 0
            self.idle = True

            return self.serving


class Queue(list):
    def __init__(self, num, MU):
        self.name = num
        self.server = Server(num, MU)
        self.time = 0
        
    def push(self, service_time, time):
        if self.server.idle and len(self) > 0:
            customer = self.pop(0)
            self.server.serve(customer, service_time)
            customer.queue_out = self.time
    
    def pull(self, next_arrival_time):
        if self.time >= next_arrival_time:
            customer = Customer()
            self.append(customer)
            customer.sys_in = self.time
            customer.queue_in = self.time
            return True
        return False

    def update(self, time):
        self.time = round(time, 1)
