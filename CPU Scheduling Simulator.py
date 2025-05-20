# CPU Scheduling Algorithms Simulator

# Function to implement First-Come First-Served (FCFS)
def fcfs(arrival_time, burst_time):
    n = len(arrival_time)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    
    # Calculate completion time
    completion_time[0] = arrival_time[0] + burst_time[0]
    for i in range(1, n):
        completion_time[i] = max(completion_time[i - 1], arrival_time[i]) + burst_time[i]

    # Calculate turnaround time and waiting time
    for i in range(n):
        turnaround_time[i] = completion_time[i] - arrival_time[i]
        waiting_time[i] = turnaround_time[i] - burst_time[i]

    # Calculate average waiting and turnaround time
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time


# Function to implement Shortest Job Next (SJN) or Shortest Job First (SJF)
def sjf(arrival_time, burst_time):
    n = len(arrival_time)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    remaining_burst_time = burst_time.copy()
    
    # Sort processes based on arrival time
    processes = sorted(range(n), key=lambda x: arrival_time[x])
    sorted_arrival_time = [arrival_time[i] for i in processes]
    sorted_burst_time = [burst_time[i] for i in processes]
    
    # Calculate waiting time and turnaround time
    time = 0
    for i in range(n):
        idx = processes[i]
        if time < sorted_arrival_time[i]:
            time = sorted_arrival_time[i]
        time += sorted_burst_time[i]
        completion_time[idx] = time
        turnaround_time[idx] = completion_time[idx] - arrival_time[idx]
        waiting_time[idx] = turnaround_time[idx] - burst_time[idx]

    # Calculate average waiting and turnaround time
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time


# Function to implement Round Robin (RR)
def round_robin(arrival_time, burst_time, quantum):
    n = len(arrival_time)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    remaining_burst_time = burst_time.copy()
    
    # Round robin scheduling
    time = 0
    queue = []
    i = 0
    while True:
        # Add processes to queue
        while i < n and arrival_time[i] <= time:
            queue.append(i)
            i += 1
        
        if len(queue) == 0:
            break
        
        # Process next in queue
        idx = queue.pop(0)
        if remaining_burst_time[idx] > quantum:
            remaining_burst_time[idx] -= quantum
            time += quantum
            # Add it back to queue
            queue.append(idx)
        else:
            time += remaining_burst_time[idx]
            completion_time[idx] = time
            remaining_burst_time[idx] = 0
            turnaround_time[idx] = completion_time[idx] - arrival_time[idx]
            waiting_time[idx] = turnaround_time[idx] - burst_time[idx]

    # Calculate average waiting and turnaround time
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time


# Function to implement Priority Scheduling
def priority_scheduling(arrival_time, burst_time, priority):
    n = len(arrival_time)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n

    processes = sorted(range(n), key=lambda x: (arrival_time[x], priority[x]))
    sorted_arrival_time = [arrival_time[i] for i in processes]
    sorted_burst_time = [burst_time[i] for i in processes]
    sorted_priority = [priority[i] for i in processes]

    # Calculate waiting time and turnaround time
    time = 0
    for i in range(n):
        idx = processes[i]
        if time < sorted_arrival_time[i]:
            time = sorted_arrival_time[i]
        time += sorted_burst_time[i]
        completion_time[idx] = time
        turnaround_time[idx] = completion_time[idx] - arrival_time[idx]
        waiting_time[idx] = turnaround_time[idx] - burst_time[idx]

    # Calculate average waiting and turnaround time
    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n

    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time


def print_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time):
    print("Waiting Times:", waiting_time)
    print("Turnaround Times:", turnaround_time)
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print()


if __name__ == '__main__':
    # Sample Input
    arrival_time = [0, 1, 2, 3, 4]
    burst_time = [5, 3, 8, 6, 2]
    priority = [3, 1, 4, 2, 5]  # Used for priority scheduling
    quantum = 2  # Time slice for round robin scheduling

    # FCFS Scheduling
    print("FCFS Scheduling:")
    waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = fcfs(arrival_time, burst_time)
    print_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)

    # SJF Scheduling
    print("SJF Scheduling:")
    waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = sjf(arrival_time, burst_time)
    print_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)

    # Round Robin Scheduling
    print("Round Robin Scheduling:")
    waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = round_robin(arrival_time, burst_time, quantum)
    print_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)

    # Priority Scheduling
    print("Priority Scheduling:")
    waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time = priority_scheduling(arrival_time, burst_time, priority)
    print_results(waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time)
