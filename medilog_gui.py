from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

import re

from medilog_objects import *

""" Widgets """


class AppWidget(qtw.QStackedWidget):
    def __init__(self, medilog):
        super(AppWidget, self).__init__()
        self.medilog = medilog
        self.color_palette = ColorPalette(index=0)

        self.setWindowTitle('Medilog')
        self.setWindowIcon(
            qtg.QIcon(r'C:/Users/rosengrp/OneDrive - weizmann.ac.il/Medilog Project/Medilog/Graphics/icon'))

        # screen size
        screen_geometry = qtw.QApplication.desktop().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        # welcome window
        self.welcome_window = WelcomeWindow(self.medilog, self.color_palette)
        self.addWidget(self.welcome_window)

        self.roster_window = None
        self.assignment_table = None
        self.request_table = None
        self.show()

    def popup_message(self, msg_title: str, msg_str: str, msg_symbol: str):
        msg = qtw.QMessageBox()
        msg.setWindowTitle(msg_title)
        msg.setText(msg_str)

        if msg_symbol == 'warning':
            msg.setIcon(qtw.QMessageBox.Warning)
        elif msg_symbol == 'critical':
            msg.setIcon(qtw.QMessageBox.Critical)
        elif msg_symbol == 'question':
            msg.setIcon(qtw.QMessageBox.Question)
        elif msg_symbol == 'information':
            msg.setIcon(qtw.QMessageBox.Information)
        else:
            msg.setIcon(qtw.QMessageBox.Information)

        aux = msg.exec_()


class WelcomeWindow(qtw.QDialog):

    def __init__(self, medilog, color_palette):
        super(WelcomeWindow, self).__init__()
        self.medilog = medilog

        self.window_width = 340
        self.window_height = 430
        self.setFixedWidth(self.window_width)
        self.setFixedHeight(self.window_height)

        self.setObjectName(u"welcome_window_dialog")
        self.setStyleSheet(
            u"QWidget#welcome_window_dialog{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(color_palette.color_list[0]) + ", stop:1 rgba"
            + str(color_palette.color_list[1]) + ")};")

        # labels
        width = 280
        height = 40
        x_position = int((self.window_width - width) / 2)
        y_position = 50
        spacing = 120

        welcome_label = qtw.QLabel(parent=self, text='Welcome')
        choose_action_label = qtw.QLabel(parent=self, text='Choose an action')

        welcome_label.setGeometry(qtc.QRect(x_position, y_position, width, height))
        choose_action_label.setGeometry(qtc.QRect(x_position, y_position + spacing, width, height))

        set_label_style(welcome_label, color_palette, 0)
        set_label_style(choose_action_label, color_palette, 1)

        # buttons
        width = 260
        height = 40
        x_position = int((self.window_width - width) / 2)
        y_position = 230
        spacing = 55

        monthly_schedule_button = qtw.QPushButton(parent=self, text='Monthly schedule')
        weekly_schedule_button = qtw.QPushButton(parent=self, text='Weekly schedule')
        statistics_button = qtw.QPushButton(parent=self, text='Statistics')

        monthly_schedule_button.setGeometry(qtc.QRect(x_position, y_position, width, height))
        weekly_schedule_button.setGeometry(qtc.QRect(x_position, y_position + spacing, width, height))
        statistics_button.setGeometry(qtc.QRect(x_position, y_position + 2 * spacing, width, height))

        set_button_style(monthly_schedule_button, color_palette, 0)
        set_button_style(weekly_schedule_button, color_palette, 0)
        set_button_style(statistics_button, color_palette, 0)

        # place elements
        ui_elements = [welcome_label,
                       choose_action_label,
                       monthly_schedule_button,
                       weekly_schedule_button,
                       statistics_button]

        [element.raise_() for element in ui_elements]

        # connections
        monthly_schedule_button.clicked.connect(self.go2roster_window)

    def go2roster_window(self):
        roster_window = RosterWindow(self.medilog)
        self.medilog.app_gui.roster_window = roster_window
        self.medilog.app_gui.addWidget(roster_window)
        self.medilog.app_gui.setCurrentIndex(self.medilog.app_gui.currentIndex() + 1)


class RosterWindow(qtw.QMainWindow):

    def __init__(self, medilog):
        super(RosterWindow, self).__init__()
        self.medilog = medilog

        self.setObjectName('roster_main_window')

        # set window size to fullscreen
        full_screen_window(self)

        # # create the central widget of the main window: tab widget
        self.tab_window = TableTabWindow(self.medilog)
        self.setCentralWidget(self.tab_window)

        # set tabs backgrounds and fonts
        self.setStyleSheet(
            u"QWidget#roster_main_window{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
            u" stop:0 rgba" + str(self.medilog.app_gui.color_palette.color_list[0]) + ", stop:1 rgba"
            + str(self.medilog.app_gui.color_palette.color_list[1]) + ")};")

        # menus
        self.menu_bar = self.menuBar()

        # file menu
        self.file_menu = self.menu_bar.addMenu('File')
        self.new_action = self.file_menu.addAction('New', self.new_roster)
        self.open_action = self.file_menu.addAction('Open', self.open_roster)
        self.save_action = self.file_menu.addAction('Save', self.save_roster)

        # export menu
        self.export_menu = self.menu_bar.addMenu('Export')
        self.create_requests_action = self.export_menu.addAction('Create requests files', self.create_requests)
        self.export_menu.addSeparator()
        self.export_action = self.export_menu.addAction('Publish', self.export_roster)

        # dock widgets

        # justice_window = qtw.QDockWidget('Justice table')
        # justice_table = qtw.QTableWidget()
        #
        # justice_window.setWidget(justice_table)
        # self.addDockWidget(qtc.Qt.RightDockWidgetArea, justice_window)
        #
        # progress_summary_window = qtw.QDockWidget('Progress summary')
        # progress_table = qtw.QTableWidget()
        # progress_summary_window.setWidget(progress_table)
        # self.addDockWidget(qtc.Qt.BottomDockWidgetArea, progress_summary_window)

    def new_roster(self):
        pass

    def open_roster(self):
        dir_path = qtw.QFileDialog.getExistingDirectory(parent=self, caption='Choose directory')
        if dir_path == '' or dir_path is None:
            return
        dir_name = dir_path.split('/')[-1]
        month, year, _ = re.split(r'(\d+)', dir_name)
        create_roster(medilog=self.medilog, month=month, year=year)

    def save_roster(self):
        pass

    def export_roster(self):
        pass

    def create_requests(self):
        create_request_file(self.medilog)


class TableTabWindow(qtw.QTabWidget):

    def __init__(self, medilog):
        super(TableTabWindow, self).__init__()
        self.medilog = medilog

        self.setObjectName('table_tab_window')

        # create and add the tabs
        self.assignment_tab = qtw.QWidget(parent=self)
        self.quota_tab = qtw.QWidget(parent=self)
        self.request_tab = qtw.QWidget(parent=self)

        self.assignment_tab.setObjectName('assignment_tab')
        self.quota_tab.setObjectName('quota_tab')
        self.request_tab.setObjectName('request_tab')

        self.addTab(self.assignment_tab, "Assignments table")
        self.addTab(self.quota_tab, "Quotas table")
        self.addTab(self.request_tab, "Requests table")

        # set tabs style
        self.assignment_tab.setStyleSheet(
            u"QWidget#assignment_tab{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(self.medilog.app_gui.color_palette.color_list[0]) + ", stop:1 rgba"
            + str(self.medilog.app_gui.color_palette.color_list[1]) + ")};")
        self.quota_tab.setStyleSheet(
            u"QWidget#quota_tab{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(self.medilog.app_gui.color_palette.color_list[0]) + ", stop:1 rgba"
            + str(self.medilog.app_gui.color_palette.color_list[1]) + ")};")
        self.request_tab.setStyleSheet(
            u"QWidget#request_tab{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(self.medilog.app_gui.color_palette.color_list[0]) + ", stop:1 rgba"
            + str(self.medilog.app_gui.color_palette.color_list[1]) + ")};")
        self.setStyleSheet(u"font: 10pt \"MS Shell Dlg 2\";")

        # add tables
        self.medilog.app_gui.assignment_table = AssignmentTable(self.assignment_tab, self.medilog)
        self.medilog.app_gui.quota_table = QuotaTable(self.quota_tab, self.medilog)


class AssignmentTable(qtw.QTableWidget):

    def __init__(self, parent, medilog):
        super(AssignmentTable, self).__init__(parent)

        self.medilog = medilog

        self.setGeometry(5, 5,
                         self.medilog.app_gui.screen_width - 15,
                         self.medilog.app_gui.screen_height - 125)
        self.setStyleSheet('font: 75 4pt \"MS Sans Serif\";')

        self.num_of_days = None
        self.num_of_shifts = None

        self.assign_combos = []

    def update_table(self):
        self.num_of_days = self.medilog.roster.num_of_days
        self.num_of_shifts = self.medilog.roster.num_of_shifts

        # set table size
        self.setRowCount(self.num_of_days)
        self.setColumnCount(self.num_of_shifts)

        shift_names = [shift.name for shift in self.medilog.roster.shifts]
        self.setHorizontalHeaderLabels(shift_names)
        [self.setColumnWidth(i, 65) for i in range(self.num_of_shifts)]
        [self.setRowHeight(i, 5) for i in range(self.num_of_days)]

        # populate table cells
        for day in range(self.num_of_days):
            for shift_id in range(self.num_of_shifts):
                combo = AssignCombo(medilog=self.medilog, day=day, shift_id=shift_id)
                self.assign_combos.append(combo)

                combo.popup_show_signal.connect(self.populate_combo)
                combo.currentTextChanged.connect(combo.combo_changed)
                combo.combo_set_signal.connect(self.update_combo)

                self.setCellWidget(day, shift_id, combo)

    @qtc.pyqtSlot(int, int)
    def populate_combo(self, day, shift_id):
        index = self.num_of_shifts * day + shift_id
        shift = self.medilog.roster.shifts[shift_id]
        available_list = get_available(self.medilog, day, shift)

        self.assign_combos[index].blockSignals(True)
        current_text = self.assign_combos[index].currentText()
        self.assign_combos[index].clear()

        self.assign_combos[index].addItems(available_list)

        # display previously assigned name
        if current_text in available_list:
            self.assign_combos[index].setCurrentText(current_text)

        self.assign_combos[index].blockSignals(False)

    @qtc.pyqtSlot(int, int, str)
    def update_combo(self, day, shift_id, physician):
        update_assignment_table(self.medilog, day, shift_id, physician)


class QuotaTable(qtw.QTableWidget):

    def __init__(self, parent, medilog):
        super(QuotaTable, self).__init__(parent)

        self.medilog = medilog

        self.setGeometry(5, 5,
                         self.medilog.app_gui.screen_width - 15,
                         self.medilog.app_gui.screen_height - 125)
        self.setStyleSheet('font: 75 4pt \"MS Sans Serif\";')

        self.num_of_physicians = None
        self.num_of_shifts = None

    def update_table(self):
        self.num_of_physicians = self.medilog.roster.num_of_physicians
        self.num_of_shifts = len(self.medilog.roster.shifts)

        # set table size
        self.setRowCount(self.num_of_physicians)
        self.setColumnCount(self.num_of_shifts)

        shift_names = [shift.name for shift in self.medilog.roster.shifts]
        self.setHorizontalHeaderLabels(shift_names)
        [self.setColumnWidth(i, 45) for i in range(self.num_of_shifts)]
        [self.setRowHeight(i, 5) for i in range(self.num_of_physicians)]


class AssignCombo(qtw.QComboBox):
    popup_show_signal = qtc.pyqtSignal(int, int)
    combo_set_signal = qtc.pyqtSignal(int, int, str)

    def __init__(self, medilog, day, shift_id):
        super(AssignCombo, self).__init__()
        self.medilog = medilog
        self.day = day
        self.shift_id = shift_id
        self.displayed_text = ''

    def showPopup(self):
        self.popup_show_signal.emit(self.day, self.shift_id)
        super(AssignCombo, self).showPopup()

    def combo_changed(self, text):
        # print('displayed_text: ' + self.displayed_text)
        # print('text: ' + text)
        if self.displayed_text == text:
            return
        else:
            self.combo_set_signal.emit(self.day, self.shift_id, text)
            self.displayed_text = text


""" Auxiliary """


def full_screen_window(window):
    screen_width = window.medilog.app_gui.screen_width
    screen_height = window.medilog.app_gui.screen_height

    window.medilog.app_gui.setWindowState(qtc.Qt.WindowMaximized)
    window.setFixedWidth(screen_width)
    window.setFixedHeight(screen_height - 65)


def create_roster(medilog, month: str, year: str):
    if medilog.roster is not None:
        print('Roster already exists.')
        return
        # add warning dialog

    medilog.roster = Roster()
    medilog.roster.load_roster(month=month, year=str(year))

    medilog.app_gui.assignment_table.update_table()
    medilog.app_gui.quota_table.update_table()


""" Appearances """


class ColorPalette:

    def __init__(self, index):
        if index == 0:
            self.color_list = [(31, 78, 120), (47, 117, 181), (112, 171, 229), (184, 214, 238), (41, 50, 65)]
            self.label_color = (255, 255, 255)
            self.button_color = (255, 255, 255)
        elif index == 1:
            self.color_list = [(60, 73, 63), (126, 141, 133), (179, 191, 184), (240, 247, 244), (99, 179, 112)]
            self.label_color = (255, 255, 255)
            self.button_color = (60, 60, 60)

    @staticmethod
    def rgb2hex(rgb_tuple):
        return '#%02x%02x%02x' % rgb_tuple


def set_label_style(label_object, palette, label_style):
    label_object.setAlignment(qtc.Qt.AlignCenter)
    if label_style == 0:
        label_object.setStyleSheet(u"font: 75 48pt \"Aharoni\";\n"
                                   "color: rgb" + str(palette.label_color) + ";")
    elif label_style == 1:
        label_object.setStyleSheet(u"color: rgb" + str(palette.label_color) + ";\n"
                                                                              "font: 24pt \"SansSerif\";")
        pass


def set_button_style(button_object, palette, button_style):
    if button_style == 0:
        button_object.setStyleSheet(u"background-color: rgb" + str(palette.color_list[-1]) + ";"
                                                                                             "border-radius:10px;"
                                                                                             "color: rgb" + str(
            palette.button_color) + ";"
                                    "font: 75 18pt \"MS Sans Serif\";")

