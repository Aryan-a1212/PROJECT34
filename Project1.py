from collections import deque  
class HotelManagementSystem:
    def __init__(self):    
        self.rooms = {}    # Dictionary to store room detail
        self.customers = {}   # Dictionary to store customer details
        self.waitlist = deque()   # Queue (deque) to manage the waitlist
        self.history = []  # Stack (list) to manage history of actions for undo functionality

    def add_room(self, room_number, room_type, price):
        if room_number in self.rooms:
            print(f"Room {room_number} already exists.")
        else:
            self.rooms[room_number] = {"type": room_type, "price": price, "status": "Available", "customer": None} 
            print(f"Room {room_number} added successfully.")

    def view_rooms(self):
        print("\nRoom Details:")
        print("Room Number | Type       | Price  | Status      | Customer")
        print("-" * 50)
        for room_number, details in self.rooms.items():
            customer = details["customer"]["name"] if details["customer"] else "N/A"
            print(f"{room_number:^11}| {details['type']:<10} | {details['price']:^6} | {details['status']:<11} | {customer}")
        print()

    def book_room(self, room_number, customer_name, customer_phone):
        if room_number not in self.rooms:
            print(f"Room {room_number} does not exist.")
            return
            
        if customer_name in self.customers:
            print(f"{customer_name} is already booked in room {self.customers[customer_name]}.")
            return

        if self.rooms[room_number]["status"] == "Available":
            self.rooms[room_number]["status"] = "Booked"
            self.rooms[room_number]["customer"] = {"name": customer_name, "phone": customer_phone}
            self.customers[customer_name] = room_number
            
            self.history.append(("BOOK", room_number, customer_name))
            print(f"Room {room_number} booked successfully for {customer_name}.")
        else:
            print(f"Room {room_number} is not available.")
            self.add_to_waitlist(customer_name, customer_phone)

    def add_to_waitlist(self, customer_name, customer_phone):
        self.waitlist.append({"name": customer_name, "phone": customer_phone})
        print(f"{customer_name} has been added to the waitlist.")

    def check_in(self, room_number):
        if room_number not in self.rooms:
            print(f"Room {room_number} does not exist.")
            return

        if self.rooms[room_number]["status"] == "Booked":
            self.rooms[room_number]["status"] = "Occupied"
            self.history.append(("CHECKIN", room_number))
            print(f"Room {room_number} is now occupied.")
        else:
            print(f"Room {room_number} is not booked yet.")

    def check_out(self, room_number):
        if room_number not in self.rooms:
            print(f"Room {room_number} does not exist.")
            return

        if self.rooms[room_number]["status"] == "Occupied":
            customer = self.rooms[room_number]["customer"]
            self.history.append(("CHECKOUT", room_number, customer))
            print(f"Customer {customer['name']} has checked out from room {room_number}.")
            self.rooms[room_number]["status"] = "Available"
            self.rooms[room_number]["customer"] = None
            self.customers.pop(customer["name"], None)

            if self.waitlist:
                next_customer = self.waitlist.popleft()
                print(f"Assigning room {room_number} to {next_customer['name']} from the waitlist.")
                self.book_room(room_number, next_customer["name"], next_customer["phone"])
        elif self.rooms[room_number]["status"] == "Booked":
            print(f"Room {room_number} is booked but not occupied yet. Please check-in first.")
        else:
            print(f"Room {room_number} is already available.")

    def undo_last_action(self):
        if not self.history:
            print("No actions to undo.")
            return

        last_action = self.history.pop()
        action_type = last_action[0]

        if action_type == "BOOK":
            room_number, customer_name = last_action[1], last_action[2]
            self.rooms[room_number]["status"] = "Available"
            self.rooms[room_number]["customer"] = None
            self.customers.pop(customer_name, None)
            print(f"Undone booking for room {room_number} by {customer_name}.")
        elif action_type == "CHECKIN":
            room_number = last_action[1]
            self.rooms[room_number]["status"] = "Booked"
            print(f"Undone check-in for room {room_number}.")
        elif action_type == "CHECKOUT":
            room_number, customer = last_action[1], last_action[2]
            self.rooms[room_number]["status"] = "Occupied"
            self.rooms[room_number]["customer"] = customer
            self.customers[customer["name"]] = room_number
            print(f"Undone check-out for room {room_number} by {customer['name']}.")

    def view_waitlist(self):
        print("\nWaitlist:")
        print("Name          | Phone")
        print("-" * 20)
        for customer in self.waitlist:
            print(f"{customer['name']:<13} | {customer['phone']}")
        print()

if __name__ == "__main__":
    system = HotelManagementSystem()

    while True:
        print("\nMenu:")
        print("1. Add Room")
        print("2. View Rooms")
        print("3. Book Room")
        print("4. Check-In")
        print("5. Check-Out")
        print("6. Undo Last Action")
        print("7. View Waitlist")
        print("8. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            room_number = input("Enter room number: ")
            room_type = input("Enter room type (Single/Double/Suite): ")
            price = float(input("Enter room price: "))
            system.add_room(room_number, room_type, price)
        elif choice == 2:
            system.view_rooms()
        elif choice == 3:
            room_number = input("Enter room number to book: ")
            customer_name = input("Enter customer name: ")
            customer_phone = input("Enter customer phone: ")
            system.book_room(room_number, customer_name, customer_phone)
        elif choice == 4:
            room_number = input("Enter room number to check-in: ")
            system.check_in(room_number)
        elif choice == 5:
            room_number = input("Enter room number to check-out: ")
            system.check_out(room_number)
        elif choice == 6:
            system.undo_last_action()
        elif choice == 7:
            system.view_waitlist()
        elif choice == 8:
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")
