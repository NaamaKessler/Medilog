from medilog_objects import *
from medilog_gui import *
import sys


class Medilog:

    def __init__(self):
        self.roster = None
        self.app_gui = AppWidget(self)


def main():
    app = qtw.QApplication(sys.argv)
    medilog = Medilog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

