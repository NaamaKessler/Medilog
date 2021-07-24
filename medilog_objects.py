from dataclasses import dataclass
import os
import pandas as pd
import pickle


class Roster:

    def __init__(self, month):
        self.seniors = None
        self.residents = None
        self.assignments = None

        self.assign_table = None
        self.request_table = None
        self.quota_table = None

        self.month = month
        self.path = os.getcwd() + '\\' + self.month

        os.chdir(self.path)

    def load_roster(self):
        self.load_physicians()
        self.load_assignments()
        self.load_requests()
        self.load_quotas()

    def load_physicians(self):
        self.seniors = []
        self.residents = []

        for senior in pd.read_csv('seniors.csv').values.tolist():
            self.seniors.append(Senior(first=senior[0], last=senior[1]))

        for resident in pd.read_csv('residents.csv').values.tolist():
            self.residents.append(Senior(first=resident[0], last=resident[1]))

    def load_assignments(self):
        assignments = pd.read_csv('assignments.csv')
        self.assign_table = AssignTable(assignments)

    def load_requests(self):
        requests = pd.read_csv('requests.csv')
        self.request_table = RequestTable(requests)

    def load_quotas(self):
        quotas = pd.read_csv('quotas.csv')
        self.quota_table = QuotaTable(quotas)


class AssignTable:

    def __init__(self, assignments):
        self.assignments = assignments
        pass


class RequestTable:

    def __init__(self, requests):
        self.requests = requests
        pass


class QuotaTable:

    def __init__(self, quotas):
        self.quotas = quotas
        pass


class Assignment:

    def __init__(self):
        pass


@dataclass
class Physician:
    first: str
    last: str

    # def __init__(self, first, last):
    #     self.first = first
    #     self.last = last

    # @property
    # def full_name(self):
    #     return self.first + ' ' + self.last
    #
    # @full_name.setter
    # def full_name(self, name):
    #     first, last = name.split(' ')
    #     self.first = first
    #     self.last = last


class Senior(Physician):
    pass


class Resident(Physician):
    pass


# if __name__ == '__main__':
#     roster = Roster('August2021')
#     roster.load_roster()
#     print(roster.seniors)



