'''
TODO:
1. Make multiple suggestion descriptions look nicer
'''

'''
    SuggestionInfo.py
    by Nathan P. Ybanez

    Creation date: 3/9/2020

    Used in Earthworm to show information about a specific suggestion
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from widget import *

_LINE_INDENT = '      ' # 6 spaces
_LINE_HEIGHT = 18
_LINE_PRESERVE_PFX = '<pre style="font-family: Consolas"; font-size=12pt>'
_LINE_PRESERVE_SFX = '</pre>'

class Ui_SuggestionInfo(object):
    def __init__(self, suggestion):
        self.suggestion = suggestion  # Suggestion information
        self.text_labels = []         # The labels that make up this suggestion

    def populate_labels(self):
        for (line_num, text) in self.suggestion.lines:
            self.add_line(line_num, text, prefix_spaces=5, highlighting='monokai')

    def clear_labels(self):
        for i in reversed(range(self.text_area.count())): 
            self.text_area.itemAt(i).widget().setParent(None)
        self.text_labels = [] # Reset the internal labels array

    def accept_changes(self, ret_data):
        self.parent.ui.accept_changes(ret_data, self.suggestion)
        self.child.close()

    # Adds a new line to the text window
    def add_line(self, line_num, text, prefix_spaces=5, highlighting='monokai'):
        # Create the label and set up the font and color
        text_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        text_label.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        text_label.setFont(font)
        text_label.setObjectName("text_line")

        # Set alignment
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(text_label.sizePolicy().hasHeightForWidth())
        text_label.setSizePolicy(sizePolicy)
        text_label.setWordWrap(False)
        text_label.setFixedHeight(_LINE_HEIGHT) # Default: 18
        text_label.setTextFormat(1) # Rich Text Format
        text_label.setAlignment(QtCore.Qt.AlignLeft)
        
        # Activate the line
        num_digits = len(str(line_num))
        highlighted_text = highlight_text(text, highlighting)
        label_text = (_LINE_PRESERVE_PFX + str(line_num)
                     + _LINE_INDENT + ''.join([' ' for i in range(5 - num_digits)])
                     + highlighted_text
                     + _LINE_PRESERVE_SFX)
        text_label.setText(label_text)
        text_label.setStyleSheet("color: rgb(255, 255, 255);\nbackground-color: rgba(255, 255, 255, 0);")
        self.text_labels.append(text_label)
        self.text_area.addWidget(self.text_labels[-1])
        self.text_labels[-1].lower() # Send to the "back" so that things can be drawn on top of this label

    def setupUi(self, SuggestionInfo):
        SuggestionInfo.setObjectName('SuggestionInfo')
        SuggestionInfo.resize(600, 600)
        SuggestionInfo.setStyleSheet('background-color: rgb(50, 50, 50);')

        # Setup label font
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        # Setup layout
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SuggestionInfo)
        self.verticalLayout_2.setObjectName('verticalLayout_2')

        # Setup title label
        self.label_title = QtWidgets.QLabel(SuggestionInfo)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet('color: rgb(255, 255, 255);')
        self.label_title.setObjectName('label_title')
        self.verticalLayout_2.addWidget(self.label_title)

        # Setup text area
        self.scrollArea = QtWidgets.QScrollArea(SuggestionInfo)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 544, 509))
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.text_area = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.text_area.setObjectName("text_area")
        self.text_area.setAlignment(QtCore.Qt.AlignTop)
        self.text_area.setSpacing(0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        # Set up reason labels
        self.label_reason1 = QtWidgets.QLabel(SuggestionInfo)
        self.label_reason1.setFont(font)
        self.label_reason1.setStyleSheet('color: rgb(255, 255, 255);')
        self.label_reason1.setObjectName('label_reason1')
        self.verticalLayout_2.addWidget(self.label_reason1)
        self.label_reason2 = QtWidgets.QLabel(SuggestionInfo)
        self.label_reason2.setFont(font)
        self.label_reason2.setStyleSheet('color: rgb(255, 255, 255);')
        self.label_reason2.setFrameStyle(QtWidgets.QFrame.Box)
        self.label_reason2.setAlignment(QtCore.Qt.AlignTop)
        self.label_reason2.setWordWrap(True)
        self.label_reason2.setObjectName('label_reason2')
        self.label_reason2.setFixedHeight(128)
        self.verticalLayout_2.addWidget(self.label_reason2)

        # Setup button pane
        self.buttons_pane = QtWidgets.QHBoxLayout()
        self.buttons_pane.setObjectName('buttons_pane')

        # Add buttons
        self.button_ok = QtWidgets.QPushButton(SuggestionInfo)
        self.button_ok.setFont(font)
        self.button_ok.setStyleSheet('background-color: rgb(100, 100, 100);\ncolor: rgb(255, 255, 255);')
        self.button_ok.setObjectName('button_ok')
        self.buttons_pane.addWidget(self.button_ok)
        self.button_fix = QtWidgets.QPushButton(SuggestionInfo)
        self.button_fix.setFont(font)
        self.button_fix.setStyleSheet('background-color: rgb(100, 100, 100);\ncolor: rgb(255, 255, 255);')
        self.button_fix.setObjectName('button_fix')
        self.buttons_pane.addWidget(self.button_fix)
        self.verticalLayout_2.addLayout(self.buttons_pane)

        # Set up text labels
        self.populate_labels()

        self.retranslateUi(SuggestionInfo)
        QtCore.QMetaObject.connectSlotsByName(SuggestionInfo)

    def retranslateUi(self, SuggestionInfo):
        _translate = QtCore.QCoreApplication.translate
        SuggestionInfo.setWindowTitle(_translate('SuggestionInfo', 'Suggestion'))
        self.label_title.setText(_translate('SuggestionInfo', 'Earthworm identified the following code fragment for revision:'))
        self.label_reason1.setText(_translate('SuggestionInfo', '\nReason(s):'))
        self.label_reason2.setText(_translate('SuggestionInfo', ''.join(self.suggestion.reasons)))
        self.button_ok.setText(_translate('SuggestionInfo', 'OK'))
        self.button_fix.setText(_translate('SuggestionInfo', 'Fix'))
