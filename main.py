from medilog_objects import *
from medilog_gui import *


class Medilog:

    def __init__(self):
        self.year = None
        self.month = None
        self.app = QApplication([])
        self.app_gui = AppWidget(self)

        self.roster = None

        self.app.exec_()


medilog = Medilog()

