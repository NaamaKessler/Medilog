from medilog_objects import *
from medilog_gui import *
import sys

BASE_PATH = r'C:\Users\rosengrp\OneDrive - weizmann.ac.il\Medilog Project\Medilog'


class Medilog:

    def __init__(self):
        self.roster = None
        self.app_gui = AppWidget(self)
        self.base_path = BASE_PATH


def main():
    app = qtw.QApplication(sys.argv)
    medilog = Medilog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

