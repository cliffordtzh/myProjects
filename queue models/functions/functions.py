import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_var(office):
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

    return LAMBDA, MU, S, LRWq, office


def simulation_results(queue, server, sojourn_times, waiting_times, time, S = 1):
    print(f"Queue {queue.name} Length: {len(queue)}")
    print(f"Server {server.name} served {server.served} customers")
    print(f"Server {server.name} is idle {server.idle}")

    total_served = server.served

    print(f"------------------------ Total Time Ran: {time:.3f} minutes ----------------------")
    print(f"Average Sojourn Time: {np.mean(sojourn_times):.3f} minutes")
    print(f"Average Waiting Time: {np.mean(waiting_times):.3f} minutes")
    print(f"Total customers served: {total_served}")


def plot_results(st, wt, sim_time, LRWq, office):
    average_waiting_times = [np.average(wt[0:i+1]) for i in range(len(wt))]
    sns.lineplot(x = np.linspace(0, sim_time, len(average_waiting_times)), y = average_waiting_times)
    plt.hlines(LRWq, 0, sim_time, label = 'Long Run Wq', color = 'red')
    plt.scatter(x = 600, y = LRWq, label = "Closing time for {office}", color = 'green', s = 20)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Average Waiting Times, Wq (minutes)")
    plt.title(f"Simulating {office} to Infinity. Minutes elapsed: {sim_time:.2f}")
    plt.legend()
    plt.show()