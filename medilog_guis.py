from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from dataclasses import dataclass

from medilog_objects import *


class AppWidget(qtw.QStackedWidget):
    def __init__(self, medilog):
        super(AppWidget, self).__init__()
        self.medilog = medilog
        self.color_palette = ColorPalette(index=0)

        self.setWindowTitle('Medilog')
        self.setWindowIcon(
            qtg.QIcon(r'C:/Users/rosengrp/OneDrive - weizmann.ac.il/Medilog Project/Medilog/Graphics/icon'))

        screen_geometry = qtw.QApplication.desktop().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.welcome_window = WelcomeWindow(self.medilog, self.color_palette)
        self.addWidget(self.welcome_window)

        self.roster_window = None

        self.show()


class WelcomeWindow(qtw.QDialog):

    def __init__(self, medilog, color_palette):
        super(WelcomeWindow, self).__init__()
        self.medilog = medilog
        self.color_palette = color_palette

        window_width = 340
        window_height = 430
        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

        self.setObjectName(u"welcome_window_dialog")
        self.setStyleSheet(
            u"QWidget#welcome_window_dialog{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(color_palette.color_list[0]) + ", stop:1 rgba"
            + str(color_palette.color_list[1]) + ")};")

        # labels
        width = 280
        height = 40
        x_position = int((window_width - width) / 2)
        y_position = 50
        spacing = 120

        welcome_label = qtw.QLabel(parent=self, text='Welcome')
        choose_action_label = qtw.QLabel(parent=self, text='Choose an action')

        welcome_label.setGeometry(qtc.QRect(x_position, y_position, width, height))
        choose_action_label.setGeometry(qtc.QRect(x_position, y_position + spacing, width, height))

        set_label_style(welcome_label, self.color_palette, 0)
        set_label_style(choose_action_label, self.color_palette, 1)

        # buttons
        width = 260
        height = 40
        x_position = int((window_width - width) / 2)
        y_position = 230
        spacing = 55

        monthly_schedule_button = qtw.QPushButton(parent=self, text='Monthly schedule')
        weekly_schedule_button = qtw.QPushButton(parent=self, text='Weekly schedule')
        statistics_button = qtw.QPushButton(parent=self, text='Statistics')

        monthly_schedule_button.setGeometry(qtc.QRect(x_position, y_position, width, height))
        weekly_schedule_button.setGeometry(qtc.QRect(x_position, y_position + spacing, width, height))
        statistics_button.setGeometry(qtc.QRect(x_position, y_position + 2 * spacing, width, height))

        set_button_style(monthly_schedule_button, self.color_palette, 0)
        set_button_style(weekly_schedule_button, self.color_palette, 0)
        set_button_style(statistics_button, self.color_palette, 0)

        # place elements
        ui_elements = [welcome_label,
                       choose_action_label,
                       monthly_schedule_button,
                       weekly_schedule_button,
                       statistics_button]

        [element.raise_() for element in ui_elements]

        # connections
        monthly_schedule_button.clicked.connect(self.go2month_schedule)

    def go2month_schedule(self):
        month = 'January'
        year = 2021
        roster = Roster(month + str(year))
        self.medilog.roster = roster
        self.medilog.roster.load_roster()

        roster_window = RosterWindow(self.medilog, self.color_palette)
        self.medilog.app_gui.roster_window = roster_window
        self.medilog.app_gui.addWidget(roster_window)
        self.medilog.app_gui.setCurrentIndex(self.medilog.app_gui.currentIndex() + 1)


class RosterWindow(qtw.QMainWindow):

    def __init__(self, medilog, color_palette):
        super(RosterWindow, self).__init__()
        self.medilog = medilog
        self.color_palette = color_palette

        self.setObjectName('roster_main_window')

        # set window size to fullscreen
        full_screen_window(self)

        # # create the central widget of the main window: tab widget
        self.tab_window = TableTabWindow(self.medilog, self.color_palette)
        self.setCentralWidget(self.tab_window)

        # set tabs backgrounds and fonts
        self.setStyleSheet(
            u"QWidget#roster_main_window{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
            u" stop:0 rgba" + str(color_palette.color_list[0]) + ", stop:1 rgba"
            + str(color_palette.color_list[1]) + ")};")

        # menu
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('File')
        self.new_action = self.file_menu.addAction('New', self.new_roster)
        self.open_action = self.file_menu.addAction('Open', self.open_roster)
        self.save_action = self.file_menu.addAction('Save', self.save_roster)

        self.file_menu.addSeparator()
        self.export_action = self.file_menu.addAction('Export', self.export_roster)

    def new_roster(self):
        pass

    def open_roster(self):
        pass

    def save_roster(self):
        pass

    def export_roster(self):
        pass


        # dock widget
        # justice_table = qtw.QWidget()
        #
        # right_dock_widget = qtw.QDockWidget('Push Helper')
        # right_dock_widget.setWidget(justice_table)
        # self.addDockWidget(qtc.Qt.RightDockWidgetArea, right_dock_widget)


class TableTabWindow(qtw.QTabWidget):

    def __init__(self, medilog, color_palette):
        super(TableTabWindow, self).__init__()
        self.medilog = medilog
        self.color_palette = color_palette

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
            u" stop:0 rgba" + str(color_palette.color_list[0]) + ", stop:1 rgba"
            + str(color_palette.color_list[1]) + ")};")
        self.quota_tab.setStyleSheet(
            u"QWidget#quota_tab{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(color_palette.color_list[0]) + ", stop:1 rgba"
            + str(color_palette.color_list[1]) + ")};")
        self.request_tab.setStyleSheet(
            u"QWidget#request_tab{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
            u" stop:0 rgba" + str(color_palette.color_list[0]) + ", stop:1 rgba"
            + str(color_palette.color_list[1]) + ")};")
        self.setStyleSheet(u"font: 10pt \"MS Shell Dlg 2\";")

        # add assignments table
        self.assignment_table = qtw.QTableView(parent=self.assignment_tab)
        self.assignment_table.setGeometry(5,
                                          5,
                                          self.medilog.app_gui.screen_width - 15,
                                          self.medilog.app_gui.screen_height - 125)


def full_screen_window(window):
    window.medilog.app_gui.setWindowState(qtc.Qt.WindowMaximized)
    window.setFixedWidth(window.medilog.app_gui.screen_width)
    window.setFixedHeight(window.medilog.app_gui.screen_height - 65)


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


class ColorPalette:

    def __init__(self, index):
        if index == 0:
            self.color_list = [(10, 34, 57), (23, 96, 135), (29, 132, 181), (83, 162, 190), (19, 46, 50)]
            self.label_color = (255, 255, 255)
            self.button_color = (255, 255, 255)
        elif index == 1:
            self.color_list = [(60, 73, 63), (126, 141, 133), (179, 191, 184), (240, 247, 244), (99, 179, 112)]
            self.label_color = (255, 255, 255)
            self.button_color = (60, 60, 60)
