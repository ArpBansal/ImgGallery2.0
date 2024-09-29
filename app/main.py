# import sys
# import os
# from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QTextEdit, QComboBox, QFileDialog, 
#                              QHBoxLayout, QVBoxLayout)
# from PyQt6.QtGui import QGuiApplication
# from PyQt6.QtQml import QQmlApplicationEngine
# from PyQt6.QtQuick import QQuickWindow
# from get_img_path
# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.window_width, self.window_height = 800, 100
#         self.setMinimumSize(self.window_width, self.window_height)

#         layout=QVBoxLayout()
#         self.setLayout(layout)

#         self.options = ('getOpenFileName()', 'getOpenFileNames()', 'getExistingDirectory()', 'getSaveFileName()')

#         self.combo = QComboBox()
#         self.combo.addItems(self.options)
#         layout.addWidget(self.combo)

#         btn = QPushButton('Launch')
#         btn.clicked.connect(self.launchDialog)
#         layout.addWidget(btn)
        
#         self.textbox = QTextEdit()
#         layout.addWidget(self.textbox)

#     def launchDialog(self):
#         option = self.options.index(self.combo.currentText())
#         match option:
#             case 0:
#                 response = self.getFileName()
#             case 1:
#                 response = self.getFileNames()
#             case 2:
#                 response = self.getDirectory()
#             case 3:
#                 response = self.getSaveFileName()
#             case _:
#                 print("Got Nothing")
#     def getFileName(self):
#         file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Image File (*.png *.jpeg *.jpg *.JPG)'
#         response = QFileDialog.getOpenFileName(
#             parent=self,
#             caption="Select a file",
#             directory='/mnt/', #os.getcwd(),
#             filter=file_filter,
#             initialFilter='Image File (*.png *.jpeg *.jpg *.JPG)'
#         )
#         self.textbox.setText(str(response))

#     def getFileNames(self):
#         file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Image File (*.png *.jpeg *.jpg *.JPG)'
#         response = QFileDialog.getOpenFileName(
#             parent=self,
#             caption="Select file(s)",
#             directory=os.getcwd(),
#             filter=file_filter,
#             initialFilter='Image File (*.png *.jpeg *.jpg *.JPG)'
#         )
#         self.textbox.setText(str(response))

#     def getDirectory(self):
#         response = QFileDialog.getExistingDirectory(
#             self,
#             caption='Select a folder'
#         )
#         self.textbox.setText(str(response))
    
#     def getSaveFileName(self):
#         file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Image File (*.png *.jpeg *.jpg *.JPG)'
#         response = QFileDialog.getSaveFileName(
#             parent=self,
#             caption='select a file',
#             directory='',
#             filter=file_filter,
#             initialFilter='Image File (*.png *.jpeg *.jpg *.JPG)'
#         )
#         self.textbox.setText(str(response))
# QQuickWindow.setSceneGraphBackend('software')
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyleSheet('''
#         QWidget {
#             font-size: 20px;
#         }
#     ''')
    
#     myApp = MyApp()
#     myApp.show()

#     try:
#         sys.exit(app.exec())
#     except SystemExit:
#         print('Closing Window...')
    # app = QGuiApplication(sys.argv)
    # engine = QQmlApplicationEngine()
    # engine.quit.connect(app.quit)
    # engine.load('./app/main.qml')
    # if not engine.rootObjects():
    #     sys.exit(-1)
    # sys.exit(app.exec())


"""
import PySimpleGUI as sg
"""

"""import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second Window")
        layout = QVBoxLayout()
        self.label = QLabel("This is the second window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.button = QPushButton("Open Second Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)
        self.second_window = None

    def show_new_window(self):
        if self.second_window is None:
            self.second_window = AnotherWindow()
        self.second_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    engine = QQmlApplicationEngine()
    engine.load(QUrl.fromLocalFile("main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
"""



'''EMBEDDINGS_DATABASE_PATH = exe/app~path'''



# print("path to images is\n" + dfs[0]['identity'][0])

from Custom_Widgets.Widgets import *
