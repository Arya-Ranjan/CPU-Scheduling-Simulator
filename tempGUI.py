import tkinter as tk
from tkinter import messagebox


class Process:
    def __init__(self, name, burst_time, arrival_time, priority=0):
        self.name = name
        self.burst_time = burst_time  # Time required for execution
        self.arrival_time = arrival_time  # Arrival time of the process
        self.priority = priority  # Priority for priority scheduling
        self.waiting_time = 0  # Waiting time
        self.turnaround_time = 0  # Turnaround time
        self.completion_time = 0  # Completion time


class CPUScheduler:
    def __init__(self):
        self.processes = []

    # FCFS Scheduling
    def fcfs_scheduling(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        for process in self.processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            process.waiting_time = current_time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            current_time += process.burst_time
            process.completion_time = current_time
        return self.processes

    # Round Robin Scheduling
    def round_robin_scheduling(self, quantum):
        queue = self.processes[:]
        current_time = 0
        while queue:
            process = queue.pop(0)
            if process.burst_time > quantum:
                process.burst_time -= quantum
                current_time += quantum
                queue.append(process)
            else:
                current_time += process.burst_time
                process.completion_time = current_time
                process.waiting_time = current_time - process.arrival_time - process.burst_time
                process.turnaround_time = process.completion_time - process.arrival_time
        return self.processes

    # Shortest Job Next Scheduling (Non-preemptive SJN)
    def sjn_scheduling(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        completed_processes = []
        while self.processes:
            ready_queue = [p for p in self.processes if p.arrival_time <= current_time]
            if ready_queue:
                ready_queue.sort(key=lambda x: x.burst_time)
                process = ready_queue.pop(0)
                self.processes.remove(process)
                process.waiting_time = current_time - process.arrival_time
                process.turnaround_time = process.waiting_time + process.burst_time
                current_time += process.burst_time
                process.completion_time = current_time
                completed_processes.append(process)
            else:
                current_time += 1
        return completed_processes

    # Shortest Job First (Non-preemptive SJF)
    def sjf_scheduling(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        completed_processes = []
        while self.processes:
            ready_queue = [p for p in self.processes if p.arrival_time <= current_time]
            if ready_queue:
                ready_queue.sort(key=lambda x: x.burst_time)
                process = ready_queue.pop(0)
                self.processes.remove(process)
                process.waiting_time = current_time - process.arrival_time
                process.turnaround_time = process.waiting_time + process.burst_time
                current_time += process.burst_time
                process.completion_time = current_time
                completed_processes.append(process)
            else:
                current_time += 1
        return completed_processes

    # Priority Scheduling
    def priority_scheduling(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        completed_processes = []
        while self.processes:
            ready_queue = [p for p in self.processes if p.arrival_time <= current_time]
            if ready_queue:
                ready_queue.sort(key=lambda x: x.priority)
                process = ready_queue.pop(0)
                self.processes.remove(process)
                process.waiting_time = current_time - process.arrival_time
                process.turnaround_time = process.waiting_time + process.burst_time
                current_time += process.burst_time
                process.completion_time = current_time
                completed_processes.append(process)
            else:
                current_time += 1
        return completed_processes


class CPUSchedulingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling Simulator")
        self.geometry("600x400")
        self.scheduler = CPUScheduler()

        # Labels and Inputs
        self.create_widgets()

    def create_widgets(self):
        self.label_name = tk.Label(self, text="Process Name:")
        self.label_name.grid(row=0, column=0)

        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=0, column=1)

        self.label_burst_time = tk.Label(self, text="Burst Time:")
        self.label_burst_time.grid(row=1, column=0)

        self.entry_burst_time = tk.Entry(self)
        self.entry_burst_time.grid(row=1, column=1)

        self.label_arrival_time = tk.Label(self, text="Arrival Time:")
        self.label_arrival_time.grid(row=2, column=0)

        self.entry_arrival_time = tk.Entry(self)
        self.entry_arrival_time.grid(row=2, column=1)

        self.label_priority = tk.Label(self, text="Priority (For Priority Scheduling):")
        self.label_priority.grid(row=3, column=0)

        self.entry_priority = tk.Entry(self)
        self.entry_priority.grid(row=3, column=1)

        # Add Process Button
        self.add_button = tk.Button(self, text="Add Process", command=self.add_process)
        self.add_button.grid(row=4, column=0, columnspan=2)

        # Dropdown for Algorithms
        self.algorithm_label = tk.Label(self, text="Select Scheduling Algorithm:")
        self.algorithm_label.grid(row=5, column=0, columnspan=2)

        self.algorithm = tk.StringVar(self)
        self.algorithm.set("FCFS")

        self.algorithm_menu = tk.OptionMenu(self, self.algorithm, "FCFS", "Round Robin", "SJN", "SJF", "Priority")
        self.algorithm_menu.grid(row=6, column=0, columnspan=2)

        # Quantum Input (For Round Robin)
        self.label_quantum = tk.Label(self, text="Quantum Time (For Round Robin):")
        self.label_quantum.grid(row=7, column=0)

        self.entry_quantum = tk.Entry(self)
        self.entry_quantum.grid(row=7, column=1)

        # Run Scheduling Button
        self.run_button = tk.Button(self, text="Run Scheduling", command=self.run_scheduling)
        self.run_button.grid(row=8, column=0, columnspan=2)

        # Output Text Box
        self.output_text = tk.Text(self, height=10, width=60)
        self.output_text.grid(row=9, column=0, columnspan=2)

    def add_process(self):
        try:
            name = self.entry_name.get()
            burst_time = int(self.entry_burst_time.get())
            arrival_time = int(self.entry_arrival_time.get())
            priority = int(self.entry_priority.get()) if self.entry_priority.get() else 0
            process = Process(name, burst_time, arrival_time, priority)
            self.scheduler.processes.append(process)

            self.entry_name.delete(0, tk.END)
            self.entry_burst_time.delete(0, tk.END)
            self.entry_arrival_time.delete(0, tk.END)
            self.entry_priority.delete(0, tk.END)

            messagebox.showinfo("Success", f"Process {name} added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")

    def run_scheduling(self):
        self.output_text.delete(1.0, tk.END)

        if not self.scheduler.processes:
            messagebox.showerror("Error", "No processes to schedule!")
            return

        selected_algorithm = self.algorithm.get()
        quantum = int(self.entry_quantum.get()) if self.entry_quantum.get() else 0

        if selected_algorithm == "FCFS":
            processes = self.scheduler.fcfs_scheduling()
        elif selected_algorithm == "Round Robin":
            if quantum <= 0:
                messagebox.showerror("Error", "Quantum time must be greater than 0 for Round Robin.")
                return
            processes = self.scheduler.round_robin_scheduling(quantum)
        elif selected_algorithm == "SJN":
            processes = self.scheduler.sjn_scheduling()
        elif selected_algorithm == "SJF":
            processes = self.scheduler.sjf_scheduling()
        elif selected_algorithm == "Priority":
            processes = self.scheduler.priority_scheduling()

        self.display_results(processes)

    def display_results(self, processes):
        self.output_text.insert(tk.END, f"{'Name':<10}{'Burst Time':<12}{'Arrival Time':<15}{'Waiting Time':<15}{'Turnaround Time':<18}{'Completion Time':<18}\n")
        self.output_text.insert(tk.END, '-' * 80 + "\n")
        for p in processes:
            self.output_text.insert(tk.END, f"{p.name:<10}{p.burst_time:<12}{p.arrival_time:<15}{p.waiting_time:<15}{p.turnaround_time:<18}{p.completion_time:<18}\n")


if __name__ == "__main__":
    app = CPUSchedulingApp()
    app.mainloop()
