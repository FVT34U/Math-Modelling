import sys
from PyQt5 import QtWidgets

from Model.MatModModel import MatModModel
from Controller.MatModController import MatModController


def main():
    app = QtWidgets.QApplication([])

    # создаём модель
    model = MatModModel()

    # создаём контроллер и передаём ему ссылку на модель
    controller = MatModController(model)

    app.exec()


if __name__ == '__main__':
    sys.exit(main())

