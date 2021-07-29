from dataclasses import dataclass, field
import os
import pandas as pd
import pickle


class Roster:

    def __init__(self, month):
        self.seniors = None
        self.residents = None
        self.assignments = None

        self.tasks = None

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
        self.load_tasks()

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

    def load_tasks(self):
        self.tasks = []
        task_table = pd.read_csv('tasks.csv')
        for i, task_name in enumerate(task_table.iloc[:, 0].values.tolist()):
            self.tasks.append(Task(name=task_name,
                                   id=i,
                                   senior=task_table.iloc[i, 2],
                                   resident=task_table.iloc[i, 3]))


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

    def is_available(self, roster, day, task):
        """
        Determine whether the physician is available for a specific task for a given day.
        :param roster: The current roster object.
        :param day: The queried day.
        :param task: The queried task.
        :return: True is available, False if not.
        """
        if self.assignment_collision(roster, day, task):
            return False
        elif self.request_collision(roster, day, task):
            return False
        elif self.unfilled_quotas(roster, day, task) == 0:
            return False
        else:
            return True

    def assignment_collision(self, roster, day, task):
        return False

    def request_collision(self, roster, day, task):
        return False

    def unfilled_quotas(self, roster, day, task):
        number_of_quotas = 1
        return number_of_quotas


class Senior(Physician):
    pass


class Resident(Physician):
    pass


@dataclass
class Task:
    name: str
    id: int
    senior: bool
    resident: bool

# if __name__ == '__main__':
#     roster = Roster('August2021')
#     roster.load_roster()
#     print(roster.seniors)



