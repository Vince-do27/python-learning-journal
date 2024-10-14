import heapq

class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = self.calc_priority()

    def calc_priority(self):
        distance = abs(ord(self.destination_station) - ord(self.start_station))
        return distance

class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0  

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, passenger): #enqueue
        heapq.heappush(self.queue, (passenger.priority, self.counter, passenger))
        self.counter += 1
        
    # Return the passenger with the highest priority
    def get(self): #deque
        if not self.is_empty():
            return heapq.heappop(self.queue)[2]
        else:
            return None

    # Peek at the highest-priority passenger without removing
    def peek(self):
        if not self.is_empty():
            return self.queue[0][2]
        return None

    def size(self):
        return len(self.queue)

    # Recalculate passenger priority based on current station
    def recalc_priorities(self, current_station):
        new_queue = []
        while self.queue:
            priority, counter, passenger = heapq.heappop(self.queue)
            passenger.priority = abs(ord(current_station) - ord(passenger.destination_station))
            heapq.heappush(new_queue, (passenger.priority, counter, passenger))
        self.queue = new_queue

class EmergencyStack:
    def __init__(self):
        self.myStack = []

    def is_empty(self):
        return len(self.myStack) == 0

    def push(self, passenger): #enqueue
        self.myStack.append(passenger)  

    def pop(self): #dequeue
        if not self.is_empty():
            return self.myStack.pop()  

    def peek(self):
        if not self.is_empty():
            return self.myStack[-1] 

class TrainSystem:
    def __init__(self, stations=['A', 'B', 'C', 'D']):
        self.stations = stations
        self.current_station = stations[0]  # Start at station 'A'
        self.priority_queue = PriorityQueue()
        self.emergency_stack = EmergencyStack()
        self.travel_times = []

    def move_to_station(self, destination_station):
        print(f"Moving from {self.current_station} to {destination_station}")
        travel_time = abs(ord(self.current_station) - ord(destination_station))
        self.current_station = destination_station
        return travel_time

    def board_passenger(self, passenger):
        self.priority_queue.add(passenger)

    # Handle emergencies first 
    def handle_passengers(self):
        if not self.emergency_stack.is_empty():
            emergency = self.emergency_stack.pop()
            print(f"Handling emergency passenger from {emergency.start_station} to {emergency.destination_station}")
            travel_time = self.move_to_station(emergency.destination_station)
            self.travel_times.append(travel_time)
            return

        # Process next passenger from the priority queue
        passenger = self.priority_queue.get()
        if passenger:
            print(f"Processing passenger from {passenger.start_station} to {passenger.destination_station}")
            travel_time = self.move_to_station(passenger.destination_station)
            self.travel_times.append(travel_time)
            # Recalculate priorities after each trip
            self.priority_queue.recalc_priorities(self.current_station)

    def add_emergency(self, passenger):
        self.emergency_stack.push(passenger)

    def average_travel_time(self):
        if self.travel_times:
            return sum(self.travel_times) / len(self.travel_times)
        return 0


# Create train system
train_system = TrainSystem()

# Add passengers
train_system.board_passenger(Passenger('A', 'C', 0))
train_system.board_passenger(Passenger('B', 'D', 1))
train_system.board_passenger(Passenger('C', 'A', 2))

# Add an emergency
train_system.add_emergency(Passenger('D', 'A', 3))

# Process passengers
for i in range(5):  
    train_system.handle_passengers()

# Get average travel time
print(f"Average travel time: {train_system.average_travel_time()} minutes")
