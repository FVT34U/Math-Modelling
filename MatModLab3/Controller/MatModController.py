from View.MatModView import MatModView


class MatModController:
    """
    Класс CplusDController представляет реализацию контроллера.
    Согласовывает работу представления с моделью.
    """
    def __init__(self, inModel):
        """
        Конструктор принимает ссылку на модель.
        Конструктор создаёт и отображает представление.
        """
        self.mModel = inModel
        self.mView = MatModView(self, self.mModel)

        self.mView.show()

    def setSettings(self):
        total_time = int(self.mView.ui.lineEdit.text())
        lines_number = int(self.mView.ui.lineEdit_4.text())
        time_ratio = float(self.mView.ui.lineEdit_2.text())
        storage_capacity = int(self.mView.ui.lineEdit_5.text())
        duration_ratio = float(self.mView.ui.lineEdit_3.text())
        erlang_parameter = int(self.mView.ui.lineEdit_6.text())

        self.mModel.set_settings(total_time, lines_number, time_ratio, storage_capacity, duration_ratio, erlang_parameter)
