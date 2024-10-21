import random
import heapq

class Passenger:
    def __init__(self, start_station, destination_station, priority):
        self.start_station = start_station
        self.destination_station = destination_station
        self.priority = priority
        self.on_board = False  # Track if the passenger is on board

    def __lt__(self, other):
        return self.priority < other.priority  

def generate_passengers(num_passengers, stations):
    passengers = []
    for i in range(num_passengers):
        start_station = random.choice(stations)
        destination_station = random.choice([station for station in stations if station != start_station])
        priority = calculate_priority(start_station, destination_station)  # Use the priority calculation
        passengers.append(Passenger(start_station, destination_station, priority))
    return passengers

def generate_emergency_passengers(num_emergency, stations):
    emergency_passengers = []
    for i in range(num_emergency):
        start_station = random.choice(stations)
        destination_station = random.choice([station for station in stations if station != start_station])
        emergency_passengers.append(Passenger(start_station, destination_station, priority=0))  # Emergency has the highest priority
    return emergency_passengers

# Priority calculation based on start and destination stations
def calculate_priority(start_station, destination_station):
    distance = abs(ord(start_station) - ord(destination_station))
    return distance  # Lower distance = higher priority

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add(self, passenger):
        heapq.heappush(self.queue, passenger)  # Push passenger onto the heap

    def get(self):
        return heapq.heappop(self.queue) if self.queue else None  # Pop the passenger with the highest priority

    def is_empty(self):
        return len(self.queue) == 0

    # Recalculate priority based on current start and destination stations
    def recalculate_priorities(self, stations):
        new_queue = []
        while not self.is_empty():
            passenger = self.get()
            passenger.priority = calculate_priority(passenger.start_station, passenger.destination_station)
            new_queue.append(passenger)

        # Push back all passengers with updated priorities
        for passenger in new_queue:
            self.add(passenger)

class EmergencyStack:
    def __init__(self):
        self.stack = []

    def push(self, passenger):
        self.stack.append(passenger)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0


class TrainSystem:
    def __init__(self, stations=['A', 'B', 'C', 'D']):
        self.stations = stations
        self.current_station = stations[0]  # Start at station 'A'
        self.priority_queue = PriorityQueue()
        self.emergency_stack = EmergencyStack()
        self.travel_times = []
        self.total_time = 0
        self.cycle = 1
        self.station_queues = {station: [] for station in stations}  # Initialize station queues

    def print_cycle_header(self):
        print(f"\nCycle {self.cycle}: Train at {self.current_station}")
        print(f"Current time: {self.total_time} minutes")
        self.cycle += 1

    def move_to_station(self, destination_station):
        if self.current_station == destination_station:
            print(f"Already at {destination_station}, no movement needed.")
            return 0  

        print(f"Moving train from {self.current_station} to {destination_station} based on priority")
        distance = abs(ord(self.current_station) - ord(destination_station))
        travel_time = distance * 10  # 10 minutes per station
        self.current_station = destination_station
        self.total_time += travel_time
        return travel_time

    def board_passenger(self, passenger):
        if self.current_station == passenger.start_station and not passenger.on_board:
            self.priority_queue.add(passenger)
            passenger.on_board = True  # Mark the passenger as on board
            print(f"New passenger from {passenger.start_station} to {passenger.destination_station} added with priority {passenger.priority}")

    def handle_passengers(self):
        while self.station_queues[self.current_station]: # Check for passengers at the current station and board them
            passenger = self.station_queues[self.current_station].pop(0)  # Get the first passenger in the queue 
            self.board_passenger(passenger)  # Attempt to board the passenger

        # Drop off passengers if any
        if not self.priority_queue.is_empty():
            passenger = self.priority_queue.get()  # Get the highest priority passenger

            # Check if the current station matches the passenger's destination
            if self.current_station == passenger.destination_station:
                print(f"Passenger from {passenger.start_station} got off at {self.current_station} after {self.total_time} minutes")
            else:
                print(f"Passenger from {passenger.start_station} will be dropped off at {passenger.destination_station}.")
                travel_time = self.move_to_station(passenger.destination_station)
                self.travel_times.append(travel_time)

                if self.current_station == passenger.destination_station:
                    print(f"Passenger from {passenger.start_station} got off at {self.current_station} after {self.total_time} minutes")
                else:
                    print(f"Passenger from {passenger.start_station} remains on the train, heading to {passenger.destination_station}.")
                
            # Recalculate priorities for remaining passengers
            self.priority_queue.recalculate_priorities(self.stations)

    def add_emergency(self, passenger):
        self.emergency_stack.push(passenger)

    def handle_emergencies(self):
        while not self.emergency_stack.is_empty():
            emergency_passenger = self.emergency_stack.pop()
            print(f"Emergency passenger from {emergency_passenger.start_station} to {emergency_passenger.destination_station} is being escorted.")

    def average_travel_time(self):
        if self.travel_times:
            return sum(self.travel_times) / len(self.travel_times)
        return 0


stations = ['A', 'B', 'C', 'D']  
train_system = TrainSystem(stations)

# Generate and queue random passengers for the initial cycle
num_passengers = 8
random_passengers = generate_passengers(num_passengers, stations)

# Introduce emergency passengers (20% of total passengers)
num_emergency_passengers = int(num_passengers * 0.2)
emergency_passengers = generate_emergency_passengers(num_emergency_passengers, stations)

# Add emergency passengers to the emergency stack
for passenger in emergency_passengers:
    train_system.add_emergency(passenger)

# Queue regular passengers at their starting stations
for passenger in random_passengers:
    train_system.station_queues[passenger.start_station].append(passenger)

# Simulate cycles
for i in range(5):  
    train_system.print_cycle_header()  # Log cycle info
    train_system.handle_passengers()  # Handle movement and drop-offs
    train_system.handle_emergencies()  # Handle emergency passengers
    print("")

# Get average travel time
print(f"\nAverage travel time: {train_system.average_travel_time()} minutes")
print(f"Total time elapsed: {train_system.total_time} minutes")
