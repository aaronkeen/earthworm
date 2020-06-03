'''
    About.py
    by Nathan P. Ybanez

    Creation date: 1/22/2020

    Used in Earthworm to show the 'Help' menu
'''


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        # Setup main window
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setFixedSize(700, 700)
        AboutDialog.setStyleSheet("background-color: rgb(50, 50, 50);")

        # Set up widgets
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(AboutDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 671, 306))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_whatis = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_whatis.setGeometry(QtCore.QRect(20, 20, 331, 31))
        
        # Set up font
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        # Set up first header
        self.label_whatis.setFont(font)
        self.label_whatis.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_whatis.setObjectName("label_whatis")
        self.label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_1.setGeometry(QtCore.QRect(20, 80, 641, 101))
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_1.setWordWrap(True)
        self.label_1.setObjectName("label_1")

        # Set up second header
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(20, 190, 641, 101))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        # Set up authors header
        self.label_aboutauthors = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_aboutauthors.setGeometry(QtCore.QRect(20, 320, 331, 31))
        font.setFamily("Consolas")
        font.setPointSize(24)
        font.setBold(True)
        self.label_aboutauthors.setFont(font)
        self.label_aboutauthors.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_aboutauthors.setObjectName("label_aboutauthors")

        # Set up third header
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setGeometry(QtCore.QRect(20, 360, 641, 61))
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        # Set up fourth header
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setGeometry(QtCore.QRect(20, 430, 641, 21))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")

        # Set up fifth header
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(20, 450, 641, 21))
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")

        # Set up sixth header
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setGeometry(QtCore.QRect(20, 470, 641, 21))
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")

        # Set up seventh header
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setGeometry(QtCore.QRect(20, 500, 641, 61))
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")

        # Set up last header
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_8.setGeometry(QtCore.QRect(20, 570, 641, 61))
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);")
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About Earthworm"))
        self.label_whatis.setText(_translate("AboutDialog", "What is Earthworm?"))
        self.label_1.setText(_translate("AboutDialog", "Earthworm is a utility designed to analyze syntactically-valid Python scripts and offer suggestions for improving the program\'s functional decomposition. Earthworm identifies code fragments that serve a separate (algorithmic) purpose from their enclosing function(s), and attempts to create an entirely new function from them. The end result is a Python script where each function does exactly one task."))
        self.label_2.setText(_translate("AboutDialog", "In general, this sort of formatting helps make programs easier to debug and organize, since each task is segmented in its own function. It also reduces the likelihood of unintended side-effects occurring when modifying parts of a program. This makes Earthworm especially useful for software development teams and also as a learning tool for students and professors."))
        self.label_aboutauthors.setText(_translate("AboutDialog", "About the Authors"))
        self.label_3.setText(_translate("AboutDialog", "The initial version of Earthworm was proposed, researched, implemented, and presented by Nupur Garg, a graduate student at California Polytechnic State University, San Luis Obispo."))
        self.label_4.setText(_translate("AboutDialog", "You can find copies of both her Thesis and code repositories below:"))
        self.label_5.setText(_translate("AboutDialog", "https://digitalcommons.calpoly.edu/theses/1759/"))
        self.label_6.setText(_translate("AboutDialog", "https://github.com/gargn/thesis"))
        self.label_7.setText(_translate("AboutDialog", "This program, written in Python, attempts to rationalize Garg\'s work into a fully-implemented User Interface, ultimately designed to make Earthworm both easier to use and more understandable."))
        self.label_8.setText(_translate("AboutDialog", "It was designed by me (Nathan P. Ybanez) as a Senior Project for my undergraduate degree in Computer Science from Cal Poly SLO."))
