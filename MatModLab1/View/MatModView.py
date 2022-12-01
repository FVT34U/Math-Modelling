from PyQt5.QtCore import pyqtSignal as SIGNAL
from PyQt5.QtWidgets import QMainWindow
from Utility.MatModObserver import MatModObserver
from Utility.MatModMeta import MatModMeta
from View.MainWindow import Ui_MainWindow, SystemParametersWindow


class MatModView(QMainWindow, MatModObserver, metaclass=MatModMeta):
    """
    Класс отвечающий за визуальное представление CplusDModel.
    """
    def __init__(self, inController, inModel, parent=None):
        """
        Конструктор принимает ссылки на модель и контроллер.
        """
        super(QMainWindow, self).__init__(parent)
        self.mController = inController
        self.mModel = inModel

        # подключаем визуальное представление
        self.ui = Ui_MainWindow()
        self.dialog = self.ui.system_parameters
        self.ui.setupUi(self)

        # регистрируем представление в качестве наблюдателя
        self.mModel.addObserver(self)

        # связываем событие завершения редактирования с методом контроллера
        self.dialog.pushButton.clicked.connect(self.mController.setSettings)

    def modelIsChanged(self):
        """
        Метод вызывается при изменении модели.
        Запрашивает и отображает значение суммы.
        """

        fig = self.mModel.get_figure()

        self.ui.setFigure(fig)
