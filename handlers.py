from book import AddressBook, Record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except ValueError:
            return "[add/change] name phone[10 digits]"
        except IndexError:
            return "Після команди введіть ім'я людини, номер якої хочете відобразити"
        except KeyError:
            return "Name not found"
    return wrapper


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):  # command = add
    name, phone, *rest = args
    record = book.find(name)
    message = 'Contact updated.'

    if record is None:
        print('Adding new contact')
        record = Record(name)
        book.add_record(record)
        message = 'Contact added'

    if phone:
        record.add_phone(phone)

    return message


@input_error
def change_contact(args, book: AddressBook):   # command = change
    """
    За цією командою бот зберігає в пам'яті новий номер телефону для контакту.
    Якщо не буде знайдений контакт -> викликається ValueError
    """
    name, old_phone, new_phone, *rest = args
    record = book.find(name)
    if record:
        # Метод edit_phone класу Record викликає виняток, якщо старий номер не знайдений
        record.edit_phone(old_number=old_phone, new_number=new_phone)
        return 'Contact updated'
    else:
        return 'Contact not found.'


@input_error
def show_phones(args, book: AddressBook) -> str:  # command = phone
    """
    Функція показує ВСІ телефонні номери у вигляді рядка для вказаного контакту.
    """
    name = args[0]
    record = book.find(name)
    if record:
        if record.phones:
            return f'Here are all phone numbers for {name}: {", ".join(p.value for p in record.phones)}'
        else:
            return f'{name} does not have any phone numbers'
    else:
        return 'Contact not found.'


@input_error
def add_birthday(args, book):  # command = add-birthday
    name, birthday_str, *rest = args
    record = book.find(name)

    if not record:
        return 'Contact not found.'

    try:
        record.add_birthday(birthday_str)
        return 'Contact now has a date of birth.'
    except ValueError as e:
        return str(e)


@input_error
def show_birthday(args, book):   # command = show-birthday
    name, *rest = args
    record = book.find(name)

    if not record:
        return 'Contact not found.'

    if not record.birthday:
        return 'This contact does not have a date of birth.'

    return record.birthday.value.strftime('%d.%m.%Y')


@input_error
def birthdays(args, book):    # command = birthdays
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return 'There are no birthdays in the nearest (working) 7 days'
    return upcoming