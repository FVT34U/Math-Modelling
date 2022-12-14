# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QSizePolicy

from View.NewSystemWindow import Ui_Dialog
import math
import tempfile
import os
from plotly.io import to_html
import plotly.graph_objs as go
import numpy as np


class Ui_MainWindow(object):
    def __init__(self):
        self.system_parameters = SystemParametersWindow()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1920, 1080)
        MainWindow.setWindowIcon(QtGui.QIcon('.\icon.ico'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(11, 9, 1909, 1071))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.web = PlotlyViewer()
        self.horizontalLayout.addWidget(self.web, 0)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)

        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action.triggered.connect(self.openNewSystemWindow)
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")

        self.menu_2_action = QtWidgets.QAction(MainWindow)
        self.menu_2_action.setObjectName("menu_2_action")
        self.menu_2_action.triggered.connect(self.openSystemParameters)
        self.menu_2_action.setEnabled(False)

        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)

        self.menu_2.addAction(self.menu_2_action)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MatMod-SolarSystem"))
        self.menu.setTitle(_translate("MainWindow", "????????"))
        self.menu_2.setTitle(_translate("MainWindow", "??????????????????"))
        self.menu_2_action.setText(_translate("MainWindow", "?????????????????? ??????????????"))
        self.action.setText(_translate("MainWindow", "?????????? ??????????????"))
        self.action_2.setText(_translate("MainWindow", "??????????????????"))
        self.action_3.setText(_translate("MainWindow", "??????????????"))

    def openNewSystemWindow(self):
        dlg = NewSystemDialog(self)
        dlg.show()
        dlg.exec()

    def openSystemParameters(self, number_of_planets: int = 1):
        if type(number_of_planets) != int:
            number_of_planets = 1
        print(number_of_planets)
        self.system_parameters.openTable()
        self.system_parameters.show()
        self.system_parameters.exec()

    def openNewSystemParameters(self, number_of_planets: int = 1):
        if type(number_of_planets) != int:
            number_of_planets = 1
        print(number_of_planets)
        self.system_parameters.setTable(num_of_planets=number_of_planets)
        self.system_parameters.show()
        self.system_parameters.exec()
        self.menu_2_action.setEnabled(True)

    def setFigure(self, fig):
        self.web.set_figure(fig)


class NewSystemDialog(QtWidgets.QDialog):
    def __init__(self, _mainWindow, parent=None):
        super(NewSystemDialog, self).__init__(parent)

        self.mainWindow = _mainWindow

        self.setWindowTitle("?????????? ??????????????")
        self.setFixedSize(350, 200)
        self.setWindowIcon(QtGui.QIcon('.\icon.ico'))

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.message = QtWidgets.QLabel("?????????????? ???????????????????? ????????????:")
        self.lineEdit = QtWidgets.QLineEdit()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self) -> None:
        try:
            value = int(self.lineEdit.text())
        except:
            value = 1
        self.mainWindow.openNewSystemParameters(value)
        self.setVisible(False)


class SystemParametersWindow(QtWidgets.QDialog):
    def __init__(self, num_of_planets: int = 1, parent=None):
        super(SystemParametersWindow, self).__init__(parent)

        self.num_of_planets = num_of_planets
        self.data = dict()

        self.setWindowTitle("?????????? ??????????????")
        self.setFixedSize(800, 420)
        self.setWindowIcon(QtGui.QIcon('.\icon.ico'))

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 781, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_3.addWidget(self.comboBox)
        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_new = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_new.setObjectName("verticalLayoutNew")
        self.label_new = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_new.setObjectName("labelNew")
        self.label_new.setText('???????????????? G')
        self.verticalLayout_new.addWidget(self.label_new)
        self.lineEdit_new = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_new.setObjectName("lineEditNew")
        self.lineEdit_new.setText('6.67e-11')
        self.verticalLayout_new.addWidget(self.lineEdit_new)

        self.horizontalLayout.addLayout(self.verticalLayout_new)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(num_of_planets)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def reject(self) -> None:
        x = np.zeros((self.num_of_planets, 1))
        y = np.zeros((self.num_of_planets, 1))
        v_x = np.zeros((self.num_of_planets, 1))
        v_y = np.zeros((self.num_of_planets, 1))
        m = np.zeros((self.num_of_planets, 1))
        G = 6.67e-11

        for j in range(0, 5):
            for i in range(0, self.num_of_planets):
                if j == 0:
                    x[i] = self.tableWidget.item(i, j).text()
                elif j == 1:
                    y[i] = self.tableWidget.item(i, j).text()
                elif j == 2:
                    v_x[i] = self.tableWidget.item(i, j).text()
                elif j == 3:
                    v_y[i] = self.tableWidget.item(i, j).text()
                elif j == 4:
                    m[i] = self.tableWidget.item(i, j).text()

        data = {
            "scheme" : self.comboBox.currentText(),
            "time_step" : self.lineEdit.text(),
            "total_time" : self.lineEdit_2.text(),
            "x": x,
            "y": y,
            "v_x": v_x,
            "v_y": v_y,
            "m": m,
            "G": G
        }

        self.data = data        
    
        return super().reject()

    def setTable(self, num_of_planets):
        self.num_of_planets = num_of_planets
        
        self.lineEdit.setText("3600")
        self.lineEdit_2.setText("31536000")
        self.comboBox.setCurrentText("????????????")

        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(num_of_planets)

        self.lineEdit_new.setText("6.67e-11")

        x = np.zeros((self.num_of_planets, 1))
        print(x)
        y = np.zeros((self.num_of_planets, 1))
        v_x = np.zeros((self.num_of_planets, 1))
        v_y = np.zeros((self.num_of_planets, 1))
        m = np.zeros((self.num_of_planets, 1))
        G = 6.67e-11

        for j in range(0, 5):
            for i in range(0, num_of_planets):
                item = QtWidgets.QTableWidgetItem()
                value = 0
                if j == 0:
                    value = int(i * 1495e8)
                    x[i] = str(value)
                elif j == 1:
                    value = 0
                    y[i] = "0"
                elif j == 2:
                    value = 0
                    v_x[i] = "0"
                elif j == 3:
                    value = 0
                    if i != 0:
                        value = math.sqrt(6.67e-11 * 1.2166e30 / (i * 1495e8))
                    v_y[i] = str(value)
                elif j == 4:
                    value = i * 0.6083e25
                    if i == 0:
                        value = "1.2166e+30"
                        m[i] = "1.2166e+30"
                    else:
                        m[i] = str(value)
                item.setText(str(value))
                self.tableWidget.setItem(i, j, item)

        data = {
            "scheme": self.comboBox.currentText(),
            "time_step": self.lineEdit.text(),
            "total_time": self.lineEdit_2.text(),
            "x": x,
            "y": y,
            "v_x": v_x,
            "v_y": v_y,
            "m": m,
            "G": G
        }

        self.data = data

    def openTable(self):
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(self.num_of_planets)

        self.lineEdit.setText(str(self.data["time_step"]))
        self.lineEdit_2.setText(str(self.data["total_time"]))
        self.lineEdit_new.setText(str(self.data["G"]))

        for j in range(0, 5):
            for i in range(0, self.num_of_planets):
                item = QtWidgets.QTableWidgetItem()
                value = 0
                if j == 0:
                    value = int(self.data["x"][i][0])
                elif j == 1:
                    value = int(self.data["y"][i][0])
                elif j == 2:
                    value = self.data["v_x"][i][0]
                elif j == 3:
                    value = self.data["v_y"][i][0]
                elif j == 4:
                    value = self.data["m"][i][0]
                item.setText(str(value))
                self.tableWidget.setItem(i, j, item)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "?????????????????? ??????????????"))
        self.pushButton.setText(_translate("Dialog", "????????????"))
        self.label_2.setText(_translate("Dialog", "?????? ???? ?????????????? (??)"))
        self.lineEdit.setText(_translate("Dialog", "3600"))
        self.label_3.setText(_translate("Dialog", "?????????? ?????????????????????????? (??)"))
        self.lineEdit_2.setText(_translate("Dialog", "31536000"))
        self.label.setText(_translate("Dialog", "???????????????????? ??????????"))
        self.comboBox.setItemText(0, _translate("Dialog", "????????????"))
        self.comboBox.setItemText(1, _translate("Dialog", "????????????-??????????????"))
        self.comboBox.setItemText(2, _translate("Dialog", "??????????"))
        self.comboBox.setItemText(3, _translate("Dialog", "????????????"))
        self.comboBox.setItemText(4, _translate("Dialog", "??????????-??????????"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "X"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Y"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Vx"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Vy"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "??????????"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Dialog", "0"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Dialog", "0"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Dialog", "0"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("Dialog", "0"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("Dialog", "1.2166e+30"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)


class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig=None):
        super().__init__()
        self.page().profile().downloadRequested.connect(self.on_downloadRequested)

        self.settings().setAttribute(self.settings().ShowScrollBars, False)
        self.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.WebGLEnabled, True)

        self.temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False)
        self.set_figure(fig)

    def set_figure(self, fig=None):
        self.temp_file.seek(0)
        if fig is None:
            fig = go.Figure()
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"

        self.temp_file.write(html)
        self.temp_file.truncate()
        self.temp_file.seek(0)
        self.load(QtCore.QUrl.fromLocalFile(self.temp_file.name))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.temp_file.close()
        os.unlink(self.temp_file.name)
        super().closeEvent(event)

    def on_downloadRequested(self, download):
        dialog = QtWidgets.QFileDialog()
        dialog.setDefaultSuffix(".png")
        path, _ = dialog.getSaveFileName(self, "Save File", os.path.join(os.getcwd(), "newplot.png"), "*.png")
        if path:
            download.setPath(path)
            download.accept()
