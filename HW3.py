from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 or value.isdigit()):
            raise ValueError("Phone number must be a 10-digit number. Please try again.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, new_phone):
        while True:
            if len(new_phone) != 10 or not new_phone.isdigit():
                print("Phone number must be a 10-digit number. Please try again.")
                new_phone = input("Enter a 10-digit phone number: ")
            else:
                self.phones[0] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_list = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_list}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for contact_name, record in self.data.items():
            if contact_name.lower() == name.lower():  # Compare in a case-insensitive manner
                return record
        return None

    def delete(self, name):
        for key in list(self.data.keys()):
            if key.lower() == name.lower():
                del self.data[key]

def parse_input(user_input):
    user_input = user_input.strip()
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter a valid command."
        except Exception as e:
            return str(e)

    return inner

# Function to add a contact to the address book
@input_error
def add_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args  # Use new_phone instead of value
        if len(new_phone) != 10 or not new_phone.isdigit():
            print("Phone number must be a 10-digit number. Please try again.")
            while True:
                new_value = input("Enter a 10-digit phone number: ")
                if len(new_value) == 10 and new_value.isdigit():
                    new_phone = new_value
                    break
        record = Record(name)
        record.add_phone(new_phone)
        address_book.add_record(record)
        return f"Contact {name} added."
    else:
        return "Invalid command. Please provide name and phone number."

# Function to change the phone number of an existing contact
@input_error
def change_contact(args, address_book):
    if len(args) == 2:
        name, new_phone = args
        if not new_phone.isdigit() or len(new_phone) != 10:
            while True:
                new_phone = input("Phone number must be a 10-digit number. Enter a 10-digit phone number: ")
                if len(new_phone) == 10 and new_phone.isdigit():
                    break
        
        record = address_book.find(name)
        if record:
            if len(record.phones) > 0:
                record.edit_phone(new_phone)  # Remove the old_phone parameter here
                return f"Phone number updated for {name}."
            else:
                return f"Contact {name} has no phone number to change."
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid command. Please provide name and new phone number."

# Function to remove a contact
@input_error
def remove_contact(args, address_book):
    if len(args) == 1:
        name = args[0]
        address_book.delete(name)  # Use the delete method to remove the contact
        return f"Contact {name} removed."
    else:
        return "Invalid command. Please provide a single name."

# Function to retrieve the phone number of a contact
@input_error
def get_phone(args, address_book):
    if len(args) == 1:
        name = args[0].lower()  # Convert the input name to lowercase
        record = address_book.find(name)
        if record:
            return f"Phone number for {record.name.value}: {record.find_phone(args[0])}"
        else:
            return f"Contact {args[0]} not found."
    else:
        return "Invalid command. Please provide a single name."

#Function to delete a phone number
@input_error
def delete_phone(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record:
            if len(record.phones) > 0:
                record.phones.clear()  # Clear all phone numbers for the contact
                return f"Phone number for {name} has been removed."
            else:
                return f"Contact {name} has no phone numbers to remove."
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid command. Please provide a name to remove all phone numbers."

# Function to list all contacts and their phone numbers
@input_error
def list_all(contacts):
    if len(contacts) > 0:
        result = "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])  # Create a formatted string to show the list of users
        return result
    else:
        return "No contacts found."

# Function to add a birthday to an existing contact
@input_error
def add_birthday(args, address_book):
    if len(args) == 2:
        name, birthday = args
        record = address_book.find(name)
        if record:
            while True:
                try:
                    record.add_birthday(birthday)
                    return f"Birthday added for {name}."
                except ValueError as e:
                    print("Invalid birthday format. Use DD.MM.YYYY.")
                    birthday = input("Enter a valid birthday date (DD.MM.YYYY): ")
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid command. Please provide name and birthday in the format DD.MM.YYYY."

# Function to show the birthday of a contact
@input_error
def show_birthday(args, address_book):
    if len(args) == 1:
        name = args[0]
        record = address_book.find(name)
        if record and record.birthday:
            return f"Birthday for {name}: {record.birthday.value}"
        elif record:
            return f"No birthday set for {name}."
        else:
            return f"Contact {name} not found."
    else:
        return "Invalid command. Please provide a single name."

# Function to show all birthdays during the next week
@input_error
def get_birthdays_per_week(address_book):
    today = datetime.today()
    
    # Find the next Monday from today
    next_monday = today + timedelta(days=(7 - today.weekday()))
    
    # Set the time to 00:00 on the next Monday
    next_monday = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Find the end of the week (Sunday at 23:59:59)
    next_sunday = next_monday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    upcoming_birthdays = []

    for record in address_book.data.values():
        if record.birthday:
            bday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y')
            bday_date = bday_date.replace(year=today.year)

            if next_monday <= bday_date <= next_sunday:
                upcoming_birthdays.append((record.name.value, bday_date.strftime('%d.%m.%Y')))

    if upcoming_birthdays:
        return "Upcoming birthdays in the next week:\n" + "\n".join([f"{name}: {birthday}" for name, birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays in the next week."

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "remove":
            print(remove_contact(args, address_book))
        elif command == "phone":
            print(get_phone(args, address_book))
        elif command == "delete-phone":
            print(delete_phone(args, address_book))
        elif command == "all":
            print(list_all(address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(get_birthdays_per_week(address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()