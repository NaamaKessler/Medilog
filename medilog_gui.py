from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QComboBox
import os


class AppWidget(QStackedWidget):
    def __init__(self):
        super(AppWidget, self).__init__()

        welcome_screen = WelcomeScreen()
        self.addWidget(welcome_screen)
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        self.show()


class WelcomeScreen(QDialog):

    def __init__(self):
        super(WelcomeScreen, self).__init__()
        ui_path = os.getcwd() + '\\' + 'ui'
        loadUi(ui_path + '\\' + 'welcome_screen.ui', self)

        self.month_btn.clicked.connect(self.go2month_schedule)

    def go2month_schedule(self):
        month_schedule = MonthSchedule()
        app_gui.addWidget(month_schedule)   # fix app_gui (not from this scope)
        app_gui.setCurrentIndex(app_gui.currentIndex() + 1)


class MonthSchedule(QDialog):

    def __init__(self):
        super(MonthSchedule, self).__init__()
        ui_path = os.getcwd() + '\\' + 'ui'
        loadUi(ui_path + '\\' + 'month_screen.ui', self)

        nColumns = 25
        nRows = 30
        self.assign_table.setColumnCount(nColumns)
        self.assign_table.setRowCount(nRows)
        self.assign_table.setHorizontalHeaderLabels(('A', 'B'))

        for i in range(nColumns):
            for j in range(nRows):
                combo = AssignCombo(self)
                self.assign_table.setCellWidget(j, i, combo)


class AssignCombo(QComboBox):

    def __init__(self, parent):
        super().__init__(parent)
        # self.addItems(items)


if __name__ == '__main__':
    app = QApplication([])
    # welcome_screen = WelcomeScreen()
    app_gui = AppWidget()
    # widget = QStackedWidget()
    # widget.addWidget(welcome_screen)

    # widget.setFixedWidth(1200)
    # widget.setFixedHeight(800)
    # widget.show()
    app.exec_()

