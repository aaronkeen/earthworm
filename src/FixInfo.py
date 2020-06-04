'''
TODO:
1. Add linter support to check Python syntax before hitting OK
2. Add text coloring and fix formatting
'''

'''
    FixInfo.py
    by Nathan P. Ybanez

    Creation date: 3/9/2020

    Used in Earthworm to show information about a specific suggestion
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from widget import *
import ast, traceback


class Ui_FixInfo(object):
    def __init__(self, suggestion):
        self.suggestion = suggestion  # Suggestion information

    def populate_text(self):
        self.populate_function()
        self.populate_invocation()

    def shift_lines_upward(self, count):
        self.suggestion.shift_lines_upward(count)

    # Fills out the function code textbox with the suggested text
    def populate_function(self):
        # Get first line's indent
        text_lines = [line[1] for line in self.suggestion.lines]
        first_indent = len(text_lines[0]) - len(text_lines[0].lstrip())
        dec_amt = first_indent - 4 if first_indent > 4 else 0 # Number of spaces to decrement each line by
        
        # Setup text box
        params_str = str(self.suggestion.params)[1:-1].replace('\'', '')
        text = 'def FUNCTION_NAME({}):\n'.format(params_str)
        for l in text_lines:
            line_leading_sp = len(l) - len(l.lstrip())
            if l.isspace():
                text += ' \n'
            elif line_leading_sp < dec_amt: # Shifting this line over would cause loss of text
                text += l
            else:
                text += l[dec_amt:]

        # Add return statement (if one exists)
        if self.suggestion.returns is not None:
            if not isinstance(self.suggestion.returns, list):
                self.suggestion.returns = [self.suggestion.returns]

            ret_str = str(self.suggestion.returns)[1:-1].replace('\'', '')
            text += '    return {}\n'.format(ret_str)
        
        self.textBox_function.setText(text)

    # Fills out the invocation textbox with the suggested text
    def populate_invocation(self):        
        # Setup text box
        params_str = str(self.suggestion.params)[1:-1].replace('\'', '')
        if self.suggestion.returns is not None:
            if not isinstance(self.suggestion.returns, list):
                self.suggestion.returns = [self.suggestion.returns]
            ret_str = str(self.suggestion.returns)[1:-1].replace('\'', '')
            text = '{} = FUNCTION_NAME({})'.format(ret_str, params_str)
        else: # No return
            text = 'FUNCTION_NAME({})'.format(params_str)

        self.textBox_invocation.setText(text)

    # Called when the user hits OK
    def custom_accept(self):
        func_text = self.textBox_function.toPlainText() # Get the text the user inputted
        invoc_text = self.textBox_invocation.toPlainText()
        ret_data = {'func_text' : func_text, 'invoc_text' : invoc_text} # Give this to the parent
        self.parent.ui.accept_changes(ret_data) # Close dialog

    def setupUi(self, FixInfo):
        # Set up window
        FixInfo.setObjectName("FixInfo")
        FixInfo.resize(600, 600)
        FixInfo.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FixInfo)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        # Font settings
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        # Set up function body text area
        self.label_function = QtWidgets.QLabel(FixInfo) # Text label for text area
        self.label_function.setFont(font)
        self.label_function.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_function.setObjectName("label_function")
        self.verticalLayout_2.addWidget(self.label_function)

        self.textBox_function = QtWidgets.QTextEdit(FixInfo)
        self.textBox_function.setFont(font)
        self.textBox_function.setStyleSheet("color: rgb(255, 255, 255);")
        self.textBox_function.setObjectName("textBox_function")
        self.verticalLayout_2.addWidget(self.textBox_function)

        # Set up function invocation text area
        self.label_invocation = QtWidgets.QLabel(FixInfo) # Text label for invocation
        self.label_invocation.setFont(font)
        self.label_invocation.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_invocation.setObjectName("label_invocation")
        self.verticalLayout_2.addWidget(self.label_invocation)

        self.textBox_invocation = QtWidgets.QTextEdit(FixInfo)
        self.textBox_invocation.setFixedHeight(64)
        self.textBox_invocation.setFont(font)
        self.textBox_invocation.setStyleSheet("color: rgb(255, 255, 255);")
        self.textBox_invocation.setObjectName("textBox_invocation")
        self.verticalLayout_2.addWidget(self.textBox_invocation)

        # Set up status label invocation text area
        '''
        self.label_status1 = QtWidgets.QLabel(FixInfo) # Text label for text area
        self.label_status1.setFont(font)
        self.label_status1.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_status1.setObjectName("label_status1")
        self.verticalLayout_2.addWidget(self.label_status1)

        self.label_status2 = QtWidgets.QLabel(FixInfo)
        self.label_status2.setFont(font)
        self.label_status2.setStyleSheet('color: rgb(255, 255, 255);')
        self.label_status2.setFrameStyle(QtWidgets.QFrame.Box)
        self.label_status2.setAlignment(QtCore.Qt.AlignTop)
        self.label_status2.setWordWrap(True)
        self.label_status2.setObjectName('label_status2')
        self.label_status2.setFixedHeight(28)
        self.verticalLayout_2.addWidget(self.label_status2)
        '''

        # Set up buttons pane
        self.buttons_pane = QtWidgets.QHBoxLayout()
        self.buttons_pane.setObjectName("buttons_pane")

        # Go button
        self.button_go = QtWidgets.QPushButton(FixInfo)
        self.button_go.setFont(font)
        self.button_go.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);")
        self.button_go.setObjectName("button_go")
        self.buttons_pane.addWidget(self.button_go)

        # Cancel button
        self.button_cancel = QtWidgets.QPushButton(FixInfo)
        self.button_cancel.setFont(font)
        self.button_cancel.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);")
        self.button_cancel.setObjectName("button_cancel")
        self.buttons_pane.addWidget(self.button_cancel)

        # Finalize layout
        self.verticalLayout_2.addLayout(self.buttons_pane)
        self.retranslateUi(FixInfo)
        QtCore.QMetaObject.connectSlotsByName(FixInfo)

    def retranslateUi(self, FixInfo):
        _translate = QtCore.QCoreApplication.translate
        FixInfo.setWindowTitle(_translate("FixInfo", "Fix Suggestion"))
        self.label_function.setText(_translate("FixInfo", "Earthworm suggests the following function body.\nChange it at your leisure:"))
        self.label_invocation.setText(_translate("FixInfo", "\nEarthworm suggests the following function invocation.\nChange it at your leisure:"))
        #self.label_status1.setText(_translate("FixInfo", "\nStatus"))
        #self.label_status2.setText(_translate("FixInfo", " "))
        self.button_go.setText(_translate("FixInfo", "Go"))
        self.button_cancel.setText(_translate("FixInfo", "Cancel"))
