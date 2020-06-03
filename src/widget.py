from PyQt5 import QtCore, QtGui, QtWidgets
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# Returns a syntax highlighted string in RTF formatting
def highlight_text(text, highlighting='monokai'):
    indent = ''.join([' ' for i in range(len(text) - len(text.lstrip()))])  # Preserve beginning indentation
    text = highlight(text, PythonLexer(), HtmlFormatter(style=highlighting, noclasses=True))

    # Remove tags
    text = text[1:]
    text = text[text.index('<') + 1:]
    text = text[text.index('<') + 1:]
    text = text[text.index('<') + 1:]
    text = text[text.index('<'):]
    text = text.replace('</pre>', '')
    text = text.replace('</div>', '')

    return indent + text


# Creates and returns a simple dialog box with an OK button (if specified)
def create_simple_dialog(parent, title, text, x, y, button=True, button_target=None):
    dialog = QtWidgets.QDialog()
    dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint) # Disable X and minimize
    hbox_master = QtWidgets.QHBoxLayout(dialog)

    # Set up text label
    dialog_label = QtWidgets.QLabel(dialog)
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setBold(True)
    dialog_label.setObjectName('dialog_label')
    dialog_label.setFont(font)
    dialog_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
    dialog_label.setStyleSheet("color: rgb(255, 255, 255);")
    dialog_label.setText(text)

    # Set up OK button
    if button:
        ok_button = QtWidgets.QPushButton('OK')
        ok_button.setStyleSheet("color: rgb(255, 255, 255);")
        ok_button.setObjectName('ok_button')
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ok_button.sizePolicy().hasHeightForWidth())
        ok_button.setSizePolicy(sizePolicy)

        if button_target is not None:
            ok_button.clicked.connect(button_target)
        else:
            ok_button.clicked.connect(dialog.close)

    # Set layout
    vbox = QtWidgets.QVBoxLayout()
    vbox.setObjectName('vbox')
    hbox = QtWidgets.QHBoxLayout()
    hbox.setObjectName('hbox')
    if button:
        hbox.addWidget(ok_button)
    vbox.addWidget(dialog_label)
    vbox.addLayout(hbox)
    hbox_master.addLayout(vbox)

    # Set up window
    dialog.setWindowTitle(title)
    dialog.setStyleSheet("background-color: rgb(50, 50, 50);")

    # Move to x, y
    dialog.move(x, y)

    return dialog


# Creates and returns a Y/N dialog box
def create_choice_dialog(parent, title, text, x, y, yes_target=None, no_target=None):
    dialog = QtWidgets.QDialog()
    dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.WindowTitleHint) # Disable X and minimize
    hbox_master = QtWidgets.QHBoxLayout(dialog)

    # Set up text label
    dialog_label = QtWidgets.QLabel(dialog)
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setBold(True)
    dialog_label.setObjectName('dialog_label')
    dialog_label.setFont(font)
    dialog_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
    dialog_label.setStyleSheet("color: rgb(255, 255, 255);")
    dialog_label.setText(text)

    # Set up Yes button
    yes_button = QtWidgets.QPushButton('Yes')
    yes_button.setStyleSheet("color: rgb(255, 255, 255);")
    yes_button.setObjectName('yes_button')
    
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(yes_button.sizePolicy().hasHeightForWidth())
    yes_button.setSizePolicy(sizePolicy)

    # Assign the target of the yes button
    if yes_target is not None:
        yes_button.clicked.connect(yes_target)
    else:
        yes_button.clicked.connect(dialog.close)

    # Set up No button
    no_button = QtWidgets.QPushButton('No')
    no_button.setStyleSheet("color: rgb(255, 255, 255);")
    no_button.setObjectName('no_button')
    
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(no_button.sizePolicy().hasHeightForWidth())
    no_button.setSizePolicy(sizePolicy)

    # Assign the target of the no button
    if no_target is not None:
        no_button.clicked.connect(no_target)
    else:
        no_button.clicked.connect(dialog.close)

    # Set layout
    vbox = QtWidgets.QVBoxLayout()
    vbox.setObjectName('vbox')
    hbox = QtWidgets.QHBoxLayout()
    hbox.setObjectName('hbox')
    hbox.addWidget(yes_button) # Add buttons
    hbox.addWidget(no_button)
    vbox.addWidget(dialog_label)
    vbox.addLayout(hbox)
    hbox_master.addLayout(vbox)

    # Set up window
    dialog.setWindowTitle(title)
    dialog.setStyleSheet("background-color: rgb(50, 50, 50);")

    # Move to x, y
    dialog.move(x, y)

    return dialog