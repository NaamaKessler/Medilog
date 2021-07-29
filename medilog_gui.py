from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QComboBox
import os
from medilog_objects import Roster
import numpy as np


class AppWidget(QStackedWidget):
    def __init__(self, medilog):
        super(AppWidget, self).__init__()

        self.medilog = medilog
        self.welcome_screen = WelcomeScreen(self.medilog)
        self.addWidget(self.welcome_screen)
        self.setFixedWidth(380)
        self.setFixedHeight(500)
        self.show()


class WelcomeScreen(QDialog):

    def __init__(self, medilog):
        super(WelcomeScreen, self).__init__()
        self.medilog = medilog

        ui_path = os.getcwd() + '\\' + 'ui'
        loadUi(ui_path + '\\' + 'welcome_screen.ui', self)

        self.month_btn.clicked.connect(self.go2month_schedule)

    def go2month_schedule(self):
        # create roster object for the current month
        # date = month_schedule.month_data.date()
        # month = date.longMonthName(1)
        # year = date.year()
        month = 'January'
        year = 2021
        roster = Roster(month + str(year))
        self.medilog.roster = roster
        self.medilog.roster.load_roster()

        month_schedule = MonthSchedule(self.medilog)
        self.medilog.app_gui.addWidget(month_schedule)
        self.medilog.app_gui.setCurrentIndex(self.medilog.app_gui.currentIndex() + 1)
        self.medilog.app_gui.setFixedWidth(1200)
        self.medilog.app_gui.setFixedHeight(800)


class MonthSchedule(QDialog):

    def __init__(self, medilog):
        super(MonthSchedule, self).__init__()
        self.medilog = medilog

        ui_path = os.path.dirname(os.getcwd()) + '\\' + 'ui'
        loadUi(ui_path + '\\' + 'month_screen.ui', self)

        self.showMaximized()
        self.nColumns = 25
        self.nRows = 30
        self.assign_table.setColumnCount(self.nColumns)
        self.assign_table.setRowCount(self.nRows)
        self.assign_table.setHorizontalHeaderLabels(('A', 'B'))

        self.combos = []
        for day in range(self.nRows):
            for task_id in range(self.nColumns):
                combo = AssignCombo(self, day=day, task_id=task_id)
                self.combos.append(combo)
                combo.popupAboutToBeShown.connect(self.populate_combo(day, task_id))
                # combo.currentTextChanged(combo.assignment_update()) ## write this function
                self.assign_table.setCellWidget(day, task_id, combo)

    def populate_combo(self, day, task_id):
        def aux_func():
            if not self.combos[index].count():
                self.combos[index].addItems(available_list)

        index = self.nColumns * day + task_id
        # names_list = ['Aharon', 'Tomer', 'Gad', 'Natalia']
        task = self.medilog.roster.tasks[task_id]
        available_list = self.get_available(day, task)

        return aux_func

    def get_available(self, day, task):
        available_list = []
        if task.senior:
            for senior in self.medilog.roster.seniors:
                if senior.is_available(self.medilog.roster, day, task):
                    available_list.append(senior.last)  ### change from .last to the actual object and handle consequences! ###

        if task.resident:
            for resident in self.medilog.roster.residents:
                if resident.is_available(self.medilog.roster, day, task):
                    available_list.append(resident.last)  ### change from .last to the actual object and handle consequences! ###

        return available_list


class AssignCombo(QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def __init__(self, parent, day, task_id):
        super().__init__(parent)
        day = day
        task_id = task_id

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(AssignCombo, self).showPopup()



