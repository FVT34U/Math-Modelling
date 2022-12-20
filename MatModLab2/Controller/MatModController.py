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
        dif_step = float(self.mView.ui.system_parameters.lineEdit.text())
        total_time = int(self.mView.ui.system_parameters.lineEdit_2.text())
        gr_type = self.mView.ui.system_parameters.comboBox.currentText()
        ind_1 = int(self.mView.ui.system_parameters.lineEdit_4.text())
        ind_2 = int(self.mView.ui.system_parameters.lineEdit_3.text())
        number = []
        up = []
        matrix = []

        for i in range(0, self.mView.ui.system_parameters.populations):
            matrix.append([])
            for j in range(0, self.mView.ui.system_parameters.populations):
                matrix[i].append(0.0)

        for i in range(0, self.mView.ui.system_parameters.populations):
            for j in range(0, self.mView.ui.system_parameters.populations):
                matrix[i][j] = float(self.mView.ui.system_parameters.tableWidget_2.item(i, j).text())

        for j in range(0, 2):
            for i in range(0, self.mView.ui.system_parameters.populations):
                if j == 0:
                    number.append(int(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))
                elif j == 1:
                    up.append(float(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))

        self.mModel.set_settings(dif_step, total_time, gr_type, ind_1, ind_2, number, up, matrix)
