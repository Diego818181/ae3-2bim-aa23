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
        self.nombre = QtWidgets.QLineEdit(self.centralwidget)
        self.nombre.setGeometry(QtCore.QRect(140, 80, 113, 23))
        self.nombre.setObjectName("nombre")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 80, 54, 15))
        self.label.setObjectName("label")
        self.nota = QtWidgets.QLineEdit(self.centralwidget)
        self.nota.setGeometry(QtCore.QRect(140, 150, 113, 23))
        self.nota.setText("")
        self.nota.setObjectName("nota")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 54, 15))
        self.label_2.setObjectName("label_2")
        self.guardar = QtWidgets.QPushButton(self.centralwidget)
        self.guardar.setGeometry(QtCore.QRect(70, 210, 211, 21))
        self.guardar.setObjectName("guardar")
        self.actualizar = QtWidgets.QPushButton(self.centralwidget)
        self.actualizar.setGeometry(QtCore.QRect(70, 262, 211, 21))
        self.actualizar.setObjectName("actualizar")
        self.listaCalificaciones = QtWidgets.QTableWidget(self.centralwidget)
        self.listaCalificaciones.setGeometry(QtCore.QRect(370, 70, 256, 192))
        self.listaCalificaciones.setObjectName("listaCalificaciones")
        self.listaCalificaciones.setColumnCount(0)
        self.listaCalificaciones.setRowCount(0)
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
        database_table_column_count = 3
        self.listaCalificaciones.setColumnCount(database_table_column_count)
        numero_filas = len(informacion)
        self.listaCalificaciones.setRowCount(numero_filas)
        for j in range(numero_filas):
            valor = informacion[j]
            for i in range(0, len(valor)):
                elemento = valor[i]
                if i == 2:  # Convertir la fecha al formato adecuado
                    elemento = datetime.strptime(elemento, "%Y-%m-%d").strftime("%d-%m-%Y")
                elemento = str(elemento)
                nuevo_registro = QtWidgets.QTableWidgetItem(elemento)
                self.listaCalificaciones.setItem(j, i, nuevo_registro)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())