from medilog_objects import *
from medilog_guis import *
import sys


class Medilog:

    def __init__(self):
        self.year = None
        self.month = None
        self.week = None
        self.roster = None

        self.app_gui = AppWidget(self)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    medilog = Medilog()
    sys.exit(app.exec_())
