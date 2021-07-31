from dataclasses import dataclass, field
import os
import pandas as pd
import calendar


class Roster:

    month_dict_abbr = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    month_dict = {month: index for index, month in enumerate(calendar.month_name) if month}

    def __init__(self, month, year):
        # handle input
        self.month = month
        self.year = year
        self.validate_input()

        self.seniors = None
        self.residents = None
        self.assignments = None
        self.shifts = None

        self.assign_table = None
        self.request_table = None
        self.quota_table = None

        self.path = os.getcwd() + '\\' + self.month + self.year  # fix to account for changing the roster
        os.chdir(self.path)

        self.number_of_days = calendar.monthrange(year=int(self.year), month=self.month_dict_abbr[self.month])[1]

    def load_roster(self):
        self.load_physicians()
        self.load_assignments()
        self.load_requests()
        self.load_quotas()
        self.load_shifts()

        print('meow')

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

    def load_shifts(self):
        self.shifts = []
        shift_table = pd.read_csv('shifts.csv')
        for i, shift_name in enumerate(shift_table.iloc[:, 0].values.tolist()):
            self.shifts.append(Shift(name=shift_name,
                                     id=i,
                                     senior=shift_table.iloc[i, 1],
                                     resident=shift_table.iloc[i, 2],
                                     active=shift_table.iloc[i, 3],
                                     passive=shift_table.iloc[i, 4],
                                     duty=shift_table.iloc[i, 5],
                                     on_call=shift_table.iloc[i, 6]))

    def validate_input(self):
        if self.month not in self.month_dict_abbr and self.month not in self.month_dict:
            raise Exception('Invalid month input.')
        if str(self.year)[0] != str(2) or str(self.year)[1] != str(0) or len(str(self.year)) > 4:
            raise Exception('Invalid year input.')


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
    assignments: list[tuple] = field(default_factory=list)

    def is_available(self, roster, day, shift):
        """
        Determine whether the physician is available for a specific shift for a given day.
        :param roster: The current roster object.
        :param day: The queried day.
        :param shift: The queried shift.
        :return: True is available, False if not.
        """
        if self.assignment_collision(roster, day, shift):
            return False
        elif self.request_collision(roster, day, shift):
            return False
        elif self.unfilled_quotas(roster, day, shift) == 0:
            return False
        else:
            return True

    def assignment_collision(self, roster, day, shift):
        return False

    def request_collision(self, roster, day, shift):
        return False

    def unfilled_quotas(self, roster, day, shift):
        number_of_quotas = 1
        return number_of_quotas


class Senior(Physician):
    pass


class Resident(Physician):
    pass


@dataclass
class Shift:
    name: str
    id: int

    senior: bool
    resident: bool

    active: bool
    passive: bool

    duty: bool
    on_call: bool





