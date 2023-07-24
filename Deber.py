import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime

conn = sqlite3.connect('base_calificaciones.db')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 514)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Campos de texto
        self.nombre = QtWidgets.QLineEdit(self.centralwidget)
        self.nombre.setGeometry(QtCore.QRect(140, 30, 113, 23))
        self.nombre.setObjectName("nombre")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 54, 15))
        self.label.setObjectName("label")
        self.nota = QtWidgets.QLineEdit(self.centralwidget)
        self.nota.setGeometry(QtCore.QRect(140, 70, 113, 23))
        self.nota.setText("")
        self.nota.setObjectName("nota")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 70, 54, 15))
        self.label_2.setObjectName("label_2")

        # Botones
        self.guardar = QtWidgets.QPushButton(self.centralwidget)
        self.guardar.setGeometry(QtCore.QRect(70, 120, 211, 21))
        self.guardar.setObjectName("guardar")
        self.actualizar = QtWidgets.QPushButton(self.centralwidget)
        self.actualizar.setGeometry(QtCore.QRect(70, 160, 211, 21))
        self.actualizar.setObjectName("actualizar")

        # Grilla con nombres de columnas
        self.listaCalificaciones = QtWidgets.QTableWidget(self.centralwidget)
        self.listaCalificaciones.setGeometry(QtCore.QRect(70, 200, 551, 261))
        self.listaCalificaciones.setObjectName("listaCalificaciones")
        self.listaCalificaciones.setColumnCount(3)
        self.listaCalificaciones.setRowCount(0)
        self.listaCalificaciones.setHorizontalHeaderLabels(["Nombre", "Nota", "Fecha"])

        # Organización de elementos
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.nombre)
        self.layout.addWidget(self.label_2)
        self.layout.addWidget(self.nota)
        self.layout.addWidget(self.guardar)
        self.layout.addWidget(self.actualizar)
        self.layout.addWidget(self.listaCalificaciones)
        self.centralwidget.setLayout(self.layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 689, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.crear_base()
        self.obtener_informacion()
        self.guardar.clicked.connect(self.guardar_informacion)
        self.actualizar.clicked.connect(self.obtener_informacion)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Nombre"))
        self.label_2.setText(_translate("MainWindow", "Nota"))
        self.guardar.setText(_translate("MainWindow", "Guardar"))
        self.actualizar.setText(_translate("MainWindow", "Actualizar"))

    def crear_base(self):
        cursor = conn.cursor()
        cadena_sql = 'CREATE TABLE Calificacion (nombre TEXT, nota INTEGER, fecha TEXT)'
        try:
            cursor.execute(cadena_sql)
        except:
            pass
        cursor.close()

    def guardar_informacion(self):
        cursor = conn.cursor()
        nombre = str(self.nombre.text())
        nota = int(self.nota.text())
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        cadena_sql = """INSERT INTO Calificacion (nombre, nota, fecha) VALUES (?, ?, ?)"""
        cursor.execute(cadena_sql, (nombre, nota, fecha_actual))
        conn.commit()
        cursor.close()

    def obtener_informacion(self):
        cursor = conn.cursor()
        cadena_consulta_sql = "SELECT * from Calificacion"
        cursor.execute(cadena_consulta_sql)
        informacion = cursor.fetchall()
        self.listaCalificaciones.setRowCount(0)
        for row_num, row_data in enumerate(informacion):
            self.listaCalificaciones.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                if col_num == 2:  # Convertir la fecha al formato adecuado
                    col_data = datetime.strptime(col_data, "%Y-%m-%d").strftime("%d-%m-%Y")
                self.listaCalificaciones.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
