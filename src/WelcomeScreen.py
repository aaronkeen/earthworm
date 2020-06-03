'''
    WelcomeScreen.py
    by Nathan P. Ybanez

    Creation date: 1/21/2020

    Used in Earthworm to show the initial options screen
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from About import Ui_AboutDialog as AboutDialog
from FileViewer import Ui_FileViewer as FileViewer
from widget import *
import sys


class CustomDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)

    # This function is called when the user presses the X (close) button
    def closeEvent(self, event):
        if self.ui.dirty: # File needs to be saved first
            diag_title = 'Earthworm'
            diag_text = 'Save changes before closing?'
            x = self.ui.scrollArea.mapToGlobal(self.ui.scrollArea.rect().center()).x() - 150 # Anchor dialog to center of window
            y = self.ui.scrollArea.mapToGlobal(self.ui.scrollArea.rect().center()).y() - 100
            save_dialog = create_choice_dialog(self.ui.scrollAreaWidgetContents, diag_title, diag_text, x, y, yes_target=self.ui.save_file)
            self.ui.save_dialog = save_dialog
            save_dialog.exec_()
            self.ui.save_dialog = None


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Main Window setup
        MainWindow.setObjectName('MainWindow')
        MainWindow.setFixedSize(767, 664)
        MainWindow.setStyleSheet('background-color: rgb(50, 50, 50);')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')

        # Set up labels
        # Copyright
        self.label_copyright = QtWidgets.QLabel(self.centralwidget)
        self.label_copyright.setGeometry(QtCore.QRect(270, 570, 251, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        font.setFamily("Consolas")
        self.label_copyright.setFont(font)
        self.label_copyright.setStyleSheet('color: rgb(255, 255, 255);\nbackground-color: rgb(50, 50, 50);')
        self.label_copyright.setObjectName('label_copyright')

        # Logo
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(30, 10, 701, 291))
        self.label_logo.setStyleSheet('background-color: rgb(50, 50, 50);')
        self.label_logo.setText('')
        self.label_logo.setPixmap(QtGui.QPixmap('img/earthworm.png'))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName('label_logo')

        # Credits
        self.label_credits = QtWidgets.QLabel(self.centralwidget)
        self.label_credits.setGeometry(QtCore.QRect(280, 600, 250, 21))
        font.setPointSize(8)
        self.label_credits.setFont(font)
        self.label_credits.setStyleSheet('color: rgb(255, 255, 255);\nbackground-color: rgb(50, 50, 50);')
        self.label_credits.setObjectName('label_credits')

        # Setup buttons
        # Open File
        self.button_open_file = QtWidgets.QPushButton(self.centralwidget)
        self.button_open_file.setGeometry(QtCore.QRect(510, 320, 201, 201))
        self.button_open_file.setStyleSheet('background-color: rgb(50, 50, 50);')
        self.button_open_file.setText('')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('img/button_open.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_open_file.setIcon(icon)
        self.button_open_file.setIconSize(QtCore.QSize(201, 201))
        self.button_open_file.setObjectName('button_open_file')

        # Open File Button Text
        self.label_open = QtWidgets.QLabel(self.centralwidget)
        self.label_open.setGeometry(QtCore.QRect(580, 530, 61, 31))
        font.setFamily('Poor Richard')
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_open.setFont(font)
        self.label_open.setStyleSheet('color: rgb(255, 255, 255);\nbackground-color: rgb(50, 50, 50);')
        self.label_open.setObjectName('label_open')
        MainWindow.setCentralWidget(self.centralwidget)

        # Help
        self.button_help = QtWidgets.QPushButton(self.centralwidget)
        self.button_help.setGeometry(QtCore.QRect(280, 320, 201, 201))
        self.button_help.setStyleSheet('background-color: rgb(50, 50, 50);\ncolor: rgb(255, 255, 255);')
        self.button_help.setText('')
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap('img/button_help.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_help.setIcon(icon1)
        self.button_help.setIconSize(QtCore.QSize(201, 201))
        self.button_help.setObjectName('button_help')

        # Help Button Text
        self.label_help = QtWidgets.QLabel(self.centralwidget)
        self.label_help.setGeometry(QtCore.QRect(345, 530, 70, 31))
        self.label_help.setFont(font)
        self.label_help.setStyleSheet('color: rgb(255, 255, 255);\nbackground-color: rgb(50, 50, 50);')
        self.label_help.setObjectName('label_help')

        # Exit
        self.button_exit = QtWidgets.QPushButton(self.centralwidget)
        self.button_exit.setGeometry(QtCore.QRect(50, 320, 201, 201))
        self.button_exit.setStyleSheet('background-color: rgb(50, 50, 50);')
        self.button_exit.setText('')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap('img/button_exit.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_exit.setIcon(icon2)
        self.button_exit.setIconSize(QtCore.QSize(201, 201))
        self.button_exit.setObjectName('button_exit')

        # Exit Button Text
        self.label_exit = QtWidgets.QLabel(self.centralwidget)
        self.label_exit.setGeometry(QtCore.QRect(130, 530, 51, 31))
        self.label_exit.setFont(font)
        self.label_exit.setStyleSheet('background-color: rgb(50, 50, 50);\ncolor: rgb(255, 255, 255);')
        self.label_exit.setObjectName('label_exit')

        # Hook up buttons to functions
        self.button_exit.clicked.connect(self.exit_program)
        self.button_help.clicked.connect(self.open_about_dialog)
        self.button_open_file.clicked.connect(self.browse_file)

        # Setup menu bars
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 767, 21))
        self.menubar.setObjectName('menubar')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Opens the 'About' menu
    def open_about_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = AboutDialog()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    # Opens the File Viewer
    def open_file_viewer(self, filename, lines):
        dialog = CustomDialog()
        dialog.ui = FileViewer(filename, lines)
        dialog.ui.setupUi(dialog)
        dialog.show()

    # Terminates the program
    def exit_program(self, MainWindow):
        sys.exit(0)

    # Opens the File Browser window to select a file to open
    def browse_file(self, MainWindow):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'Python Scripts (*.py)',)

        # Leave if the user cancelled
        if filename == '':
            return

        # Open file and get data out
        lines = []
        i = 1
        with open(filename, 'r') as f_in:
            for line in f_in:
                lines.append((str(i), line))
                i += 1

        # Open up the text view
        self.open_file_viewer(filename, lines)

    # Move UI elements into place
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'Earthworm'))
        self.label_copyright.setText(_translate('MainWindow', '© 2020 Nathan Ybanez, Nupur Garg'))
        self.label_credits.setText(_translate('MainWindow', 'Created with PyQt5 and Qt Designer'))
        self.label_exit.setText(_translate('MainWindow', 'Exit'))
        self.label_help.setText(_translate('MainWindow', 'About'))
        self.label_open.setText(_translate('MainWindow', 'Open'))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
