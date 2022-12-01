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
        total_time = int(self.mView.ui.system_parameters.lineEdit_2.text())
        step = int(self.mView.ui.system_parameters.lineEdit.text())
        scheme = self.mView.ui.system_parameters.comboBox.currentText()

        m = []
        x = []
        y = []
        v_x = []
        v_y = []
        G = float(self.mView.ui.system_parameters.lineEdit_new.text())

        for j in range(0, 5):
            for i in range(self.mView.ui.system_parameters.num_of_planets):
                if j == 0:
                    x.append(int(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))
                if j == 1:
                    y.append(int(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))
                if j == 2:
                    v_x.append(float(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))
                if j == 3:
                    v_y.append(float(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))
                if j == 4:
                    m.append(float(self.mView.ui.system_parameters.tableWidget.item(i, j).text()))

        self.mView.ui.system_parameters.data = {
            "scheme": self.mView.ui.system_parameters.comboBox.currentText(),
            "time_step": int(self.mView.ui.system_parameters.lineEdit.text()),
            "total_time": int(self.mView.ui.system_parameters.lineEdit_2.text()),
            "x": x,
            "y": y,
            "v_x": v_x,
            "v_y": v_y,
            "m": m,
            "G": G
        }

        self.mView.ui.system_parameters.close()

        self.mModel.setSettings(m, x, y, v_x, v_y, G, total_time, step, scheme)
