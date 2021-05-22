import pandas as pd


class Roster:

    def __init__(self):
        pass


class AssignTable:

    def __init__(self):
        pass


class RequestTable:

    def __init__(self):
        pass


class QuotaTable:

    def __init__(self):
        pass


class Physician:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return self.first + ' ' + self.last

    @full_name.setter
    def full_name(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last


class Senior(Physician):
    pass


class Resident(Physician):
    pass


if __name__ == '__main__':
    doc1 = Physician('Henry', 'Loyed')
    print(doc1.full_name)
    doc1.full_name = 'Josh Rosie'
    print(doc1.full_name)


