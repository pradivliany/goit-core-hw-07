from collections import UserDict
from datetime import datetime
from birthday_functions import get_upcoming_birthdays


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone_number: str) -> None:
        super().__init__(phone_number)
        self._validate_phone()

    def _validate_phone(self):
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError('Phone number should have 10 digits')


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_datetime = datetime.strptime(value, '%d.%m.%Y')
            self.value = birthday_datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_birthday(self, birthday_str):
        if self.birthday is not None:
            raise ValueError("This contact already has a date of birth.")
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        self.phones = [el for el in self.phones if el.value != phone_number]

    def edit_phone(self, old_number: str, new_number: str) -> None:
        old_phone = Phone(old_number)
        new_phone = Phone(new_number)

        for phone in self.phones:
            if phone.value == old_phone.value:
                phone.value = new_phone.value
                return

        raise ValueError('Old phone number {} was not found'.format(old_number))

    def find_phone(self, phone_number: str) -> None | Phone:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, persons_name: str) -> Record | None:
        return self.data.get(persons_name)

    def delete(self, persons_name: str) -> None:
        self.data.pop(persons_name, None)

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict[str, str]]:
        return get_upcoming_birthdays(self.data.values(), days)

    def __str__(self):
        txt = 'Address Book:\n'
        if not self.data:
            return txt + 'Address book is empty'
        result = '\n'.join(str(el) for el in self.data.values())
        txt += result
        return txt
