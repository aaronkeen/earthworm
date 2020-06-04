'''
TODO:
1. Make it so the resolutions of all windows are a percent of the screen
2. Make it so the pop-up dialogs center on the screen
3. Add extra spaces to the end of labels after Analyze so that the scrollbar can reach and show the entire highlighted area
'''

'''
    FileViewer.py
    by Nathan P. Ybanez

    Creation date: 1/27/2020

    Used in Earthworm to show the contents of the file
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from SuggestionInfo import Ui_SuggestionInfo as SuggestionInfo
from FixInfo import Ui_FixInfo as FixInfo
from gargn_earthworm.src.decomposer import generate_suggestions
from widget import *
from suggestion import *

import time
import random

_LINE_INDENT = '      ' # 6 spaces
_LINE_HEIGHT = 18
_ANALYZE_LINEEND_PADDING = 25  # Add 10 spaces to the end of line after analyzing
_LINE_PRESERVE_PFX = '<pre style="font-family: Consolas"; font-size=12pt>'
_LINE_PRESERVE_SFX = '</pre>'
_COLOR_HIGHLIGHT = "color: rgb(255, 75, 50);"


class ScrollAreaContents(QtWidgets.QWidget):
    def __init__(self):
        self.colors = []
        self.has_analyzed = False
        self.coords = []
        self.suggestions = []
        self.text_labels = []
        #self.checkboxes = []
        self.dialogs = []
        self.info_buttons = []
        super(ScrollAreaContents, self).__init__()

    # Pick random colors to use for the suggestions
    def get_colors(self, suggestions):
        colors = []
        for i in range(len(self.suggestions)):
            colors.append(self.pick_random_color()) # Get a random color
        return colors

    # Returns a random color
    def pick_random_color(self):
        min_color = 100 # Min RGB value
        max_color = 255 # Max RGB value

        return QColor(random.randint(min_color, max_color), 
                      random.randint(min_color, max_color),
                      random.randint(min_color, max_color))

    # Returns the RGB components of the given QColor object
    def extract_color(self, color):
        return color.red(), color.green(), color.blue()

    # Creates a new button
    def add_info_button(self, x, y, target=None):
        # Create new button and setup fonts and color
        new_button = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        new_button.setFixedSize(15,15)
        new_button.setFont(font)
        new_button.setStyleSheet("background-color: rgb(100, 100, 100);\ncolor: rgb(255, 255, 255);")

        # Set the text and attach button to the interface
        self.info_buttons.append(new_button)
        new_button.setText('?')
        new_button.move(x, y)
        new_button.raise_()
        new_button.show()

        # Set target
        if target is not None:
            new_button.clicked.connect(target)

    # Adds a checkbox at the (x, y) coordinates
    def add_checkbox(self, x, y):
        checkbox = QtWidgets.QCheckBox(self)
        checkbox.setGeometry(QtCore.QRect(x, y, 20, 20))
        checkbox.setText("")
        checkbox.setObjectName("checkBox")
        checkbox.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        checkbox.raise_()
        checkbox.show()
        self.checkboxes.append(checkbox)

    # Resets the internal state of this widget
    def reset_state(self):
        self.colors = []
        self.has_analyzed = False
        self.coords = []
        self.suggestions = []
        self.text_labels = []
        self.clear_dialogs()
        #self.clear_checkboxes()
        self.clear_info_buttons()

    # Clears any info dialogs
    def clear_dialogs(self):
        for diag in self.dialogs: 
            diag.close()
        self.dialogs = [] # Reset the internal dialog array

    # Clears any fix dialogs
    def clear_fix_dialogs(self):
        for diag in self.fix_dialogs: 
            diag.close()
        self.fix_dialogs = [] # Reset the internal dialog array

    # Clears any checkboxes
    def clear_checkboxes(self):
        for checkbox in self.checkboxes: 
            checkbox.close()
        self.checkboxes = [] # Reset the internal checkbox array

    # Clears any info_buttons
    def clear_info_buttons(self):
        for info_button in self.info_buttons: 
            info_button.close()
        self.info_buttons = [] # Reset the internal checkbox array

    # Overrides paintEvent()
    def paintEvent(self, event):
        if self.has_analyzed:
            qp = QPainter()
            qp.begin(self)

            # Draw all the rectangles
            for i in range(len(self.coords)):
                (x, y, w, h) = self.coords[i]
                # Set up pen
                color = self.colors[i]
                r, g, b = self.extract_color(self.colors[i])
                qp.setBrush(QBrush(QColor(r, g, b, 15), Qt.SolidPattern)) # Semi-transparent background
                qp.setPen(QPen(color, 2, Qt.SolidLine)) # Fully opaque border
                qp.drawRect(x, y, w, h) # Draw rectangle

            qp.end()

    # Returns the length of the longest line in the set of labels
    def get_longest_width(self, labels):
        longest = 0
        for label in labels:
            # sizeHint = the 'actual' size of the widget based on its contents
            width = label.sizeHint().width() + 100
            if width > longest:
                longest = width

        return longest

    # Gets the coordinates and sizes of all the suggestion areas
    def get_suggestion_coords(self):
        coords = []
        for suggestion in self.suggestions:
            # Get labels corresponding to the suggestion
            labels = self.text_labels[suggestion.start - 1 : suggestion.end]

            # Get coordinates, width, height for box
            x = 40  # 40 to get past the line number
            y = labels[0].y()  # First label is the origin
            w = self.get_longest_width(labels) + 25 # Width is as long as the longest line
            h = len(labels) * _LINE_HEIGHT # Each line is 18 tall

            # Adjustment for completely nested suggestions
            for (x_coord, y_coord, width, height) in coords:
                max_y = y_coord + height
                # Nested suggestion if this y-coord is completely contained in "parent"s y-range
                if y >= y_coord and (y + h) <= max_y:
                    x = x_coord + 20 # Slightly shift dimensions so this rect is 'inside'
                    w = width - 60

            # Adjustment for semi-nested suggestions with the same start point
            for (x_coord, y_coord, width, _) in coords:
                if x == x_coord and y == y_coord:
                    x += 20
                    w = width + 20

            # Adjustment for semi-nested suggestions with the same width
            for (_, y_coord, width, height) in coords:
                if w == width and y >= y_coord and y <= y_coord + height:
                    w += 20

            # Final adjustment for cases where width ends at exact same x-coord
            for (x_coord, _, width, _) in coords:
                if x + w == x_coord + width:
                    w += 20

            coords.append((x, y, w, h))

        return coords
        

class Ui_FileViewer(object):
    def __init__(self, filename, lines):
        self.has_analyzed = False  # True if user ran an 'Analyze'
        self.suggestions = []      # Suggestions from latest Analyze
        self.suggestion_infos = [] # Dialog boxes with info about suggestions
        self.fix_infos = []        # Dialog boxes with info about fixes
        self.buttons = []          # Current initialized buttons
        self.filename = filename   # Name of opened file
        self.lines = lines         # Raw text data w/ line numbers
        self.text_labels = []      # RTF-formatted Text labels
        self.dirty = False         # Dirty file needs saving before close
        self.FileViewer = None     # Reference to FileViewer object
        self.save_dialog = None    # Global flag to specify if a "save before quit" dialog is open (None = nothing open)

    def setupUi(self, FileViewer):
        # Setup main window
        self.FileViewer = FileViewer
        FileViewer.setObjectName("FileViewer")
        FileViewer.resize(900, 1000)
        FileViewer.setStyleSheet("background-color: rgb(50, 50, 50);")

        # Setup layout(s)
        self.gridLayout = QtWidgets.QGridLayout(FileViewer)
        self.gridLayout.setObjectName("gridLayout")
        self.button_pane = QtWidgets.QHBoxLayout()
        self.button_pane.setObjectName("button_pane")
        self.gridLayout.addLayout(self.button_pane, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(FileViewer)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = ScrollAreaContents()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 722, 854))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Setup main text area
        self.text_area = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.text_area.setObjectName("text_area")
        self.text_area.setAlignment(QtCore.Qt.AlignTop)
        self.text_area.setSpacing(0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 1)

        # Populate text area with the opened file's lines
        self.populate_lines(self.lines, prefix_spaces=5)

        # Create buttons
        self.add_button(text='Open File', icon_path='../src/img/icon_open.png', target=self.open_file, tooltip_text='Open a file to analyze')
        self.add_button(text='Analyze', icon_path='../src/img/icon_analyze.png', target=self.analyze, tooltip_text='Analyze the file and identify code fragments to separate')
        #self.add_button(text='Select All', icon_path='../src/img/icon_selectall.png', target=None)
        #self.add_button(text='Fix Selected', icon_path='../src/img/icon_fix.png', target=None)
        self.add_button(text='Save As', icon_path='../src/img/icon_saveas.png', target=self.save_file, tooltip_text='Save the currently opened file')

        # Setup tooltips
        QtWidgets.QToolTip.setFont(QtGui.QFont('Consolas', 10))

        self.retranslateUi(FileViewer)
        QtCore.QMetaObject.connectSlotsByName(FileViewer)

    # Resets this widget's state
    def reset_state(self):
        self.clear_lines()
        self.has_analyzed = False
        self.dirty = False
        #self.ret_data = {}
        self.suggestion_infos = []
        self.fix_infos = []
        self.suggestions = []

    # Fills the text window with labels from the current set of lines
    def populate_lines(self, lines, prefix_spaces=5, suffix_spaces=0):
        self.clear_lines()
        for (line_num, text) in lines:
            self.add_line(line_num, text, prefix_spaces=prefix_spaces, suffix_spaces=suffix_spaces, highlighting='monokai')

    # Resets the scrollbar to the top of the window
    def reset_scrollbar(self):
        vbar = self.scrollArea.verticalScrollBar()
        vbar.setValue(vbar.minimum())

    # Saves the file to the disk
    def save_file(self):
        # Ask user for filename to save as
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File')
        if filename == '': # Leave if the user cancelled
            return

        # Save the file
        with open(filename, 'w') as f:
            lines = [text for (_, text) in self.lines]
            # Add \n if the line doesn't have one
            text = ''.join(['{}\n'.format(line) if len(line) > 0 and line[-1] != '\n' else line for line in lines])
            f.write(text)

        # File isn't dirty anymore
        self.dirty = False
        self.filename = filename # Set window title
        self.set_window_title('Earthworm (' + self.truncate_filename() + ')')

        if self.save_dialog is not None: # We came from a dialog to get here. Close it
            self.save_dialog.close()

    # Opens the File Browser window to select a file to open
    def open_file(self):
        # Ask user for filename to open
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'Python Scripts (*.py)',)
        if filename == '': # Leave if the user cancelled
            return

        # File is 'dirty', needs saving before opening new one
        if self.dirty:
            diag_title = 'Earthworm'
            diag_text = 'Save changes before closing?'
            x = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).x() - 150 # Anchor dialog to center of window
            y = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).y() - 100
            save_dialog = create_choice_dialog(self.scrollAreaWidgetContents, diag_title, diag_text, x, y, yes_target=self.save_file)
            self.save_dialog = save_dialog
            save_dialog.exec_()

        self.save_dialog = None

        # Open file and get lines out
        lines = []
        i = 1
        with open(filename, 'r') as f_in: 
            for line in f_in:
                lines.append((str(i), line))
                i += 1

        # Reset everything
        self.reset_state()
        self.lines = lines
        self.filename = filename
        self.scrollAreaWidgetContents.reset_state() # Turn off old analyze boxes
        self.reset_scrollbar()

        # Set new window title
        self.set_window_title("Earthworm (" + self.truncate_filename() + ")")

        # Populate window with new lines
        self.populate_lines(self.lines, prefix_spaces=5)
        
    # Changes the window title
    def set_window_title(self, title):
        _translate = QtCore.QCoreApplication.translate
        self.FileViewer.setWindowTitle(_translate("FileViewer", title))

    def update_suggestion_indices(self):
        for i in range(len(self.suggestions)):
            self.suggestions[i].index = i

    # Called when a SuggestionInfo returns changes
    def accept_changes(self, ret_data, suggestion):
        for s in self.suggestion_infos:
            s.close() # Close suggestion windows

        # Get returned data
        func_text = ret_data['func_text']
        invoc_text = ret_data['invoc_text'] + '\n'

        # Get the index of this suggestion
        s_index = suggestion.index

        # Put the invocation text where the suggestion begins
        returns = True if suggestion.returns is not None else False
        st = suggestion.start
        end = suggestion.end
        num_sp = len(suggestion.lines[0][1]) - len(suggestion.lines[0][1].lstrip())
        st_spaces = ''.join([' ' for i in range(num_sp)]) # Calculate indent
        self.lines[st - 1] = (str(st), st_spaces + invoc_text) # Replace the line

        # Now remove the rest of the original code
        for i in range(st+1, end+1):
            self.lines.pop(st)

        # Move the lines to the start of the file
        ins_index = -1
        for i in range(len(self.lines)):
            spl = self.lines[i][1].split()
            if len(spl) == 0:
                continue

            # Function or class definition
            if spl[0] in ['class', 'def']:
                ins_index = i
                break

        # Now insert the new code
        ins_before = self.lines[:ins_index]
        ins_after = self.lines[ins_index:]

        ins = []
        ins.append(('1', '\n')) # Mandatory blank line before
        func_lines = func_text.split('\n')
        for line in func_lines:
            ins.append(('1', line+'\n'))
        ins.append(('1', '\n')) # Mandatory blank line after

        self.lines = ins_before + ins + ins_after

        # Renumber the lines because code was removed/added
        self.update_linenos()

        # Remove this suggestion from the pool
        self.remove_suggestion(s_index)

        # Remove any suggestions that were nested/overlapping with this suggestion
        while True:
            found = False
            for s in self.suggestions:
                # Is this suggestion nested/overlapping with the original one we removed?
                # Overlapping if either the start or end point are between the fixed suggestion
                overlapping = (s.start >= st and s.start <= end) or (s.end >= st and s.end <= end)
                if overlapping:
                    found = True
                    self.remove_suggestion(s.index) # Remove the suggestion and its box
                    break
            # No new suggestions to remove
            if not found:
                break

        # Shift all remaining suggestion line numbers
        new_code_length = len(ins) # How many new lines were inserted
        for s in self.suggestions:
            # Figure out how much to shift by
            if s.start > end: # Suggestion is BELOW, code shifts up (from prev removal) also
                self.suggestions[s.index].shift_lines(direction='up', count=(end - st))

            # Update text labels
            self.suggestions[s.index].shift_lines(direction='down', count=new_code_length)
            self.suggestion_infos[s.index].ui.clear_labels()
            self.suggestion_infos[s.index].ui.populate_labels()

        # Now recalculate coordinates and redraw boxes
        self.scrollAreaWidgetContents.suggestions = self.suggestions
        self.scrollAreaWidgetContents.text_labels = self.text_labels
        self.scrollAreaWidgetContents.coords = self.scrollAreaWidgetContents.get_suggestion_coords()
        for i in range(len(self.scrollAreaWidgetContents.coords)):
            (x, y, _, _) = self.scrollAreaWidgetContents.coords[i]
            self.scrollAreaWidgetContents.info_buttons[i].move(x+3, y+2)

        # Mark file as 'dirty' (need to save before closing or loading new file)
        self.dirty = True
        self.set_window_title('Earthworm (' + self.truncate_filename() + ')*')

        # Repopulate the lines
        self.populate_lines(self.lines)

    # Deletes the suggestion and its associated information (dialogs and drawn boxes)
    def remove_suggestion(self, s_index):
        self.suggestions.pop(s_index)
        self.suggestion_infos.pop(s_index)
        self.fix_infos.pop(s_index)

        # Remove the suggestion's box
        self.scrollAreaWidgetContents.coords.pop(s_index)
        self.scrollAreaWidgetContents.info_buttons[s_index].setParent(None)
        self.scrollAreaWidgetContents.info_buttons.pop(s_index)

        # A suggestion was removed, update the indices
        self.update_suggestion_indices()

    # Recalculates all the line numbers from top to bottom
    def update_linenos(self):
        for i in range(len(self.lines)):
            self.lines[i] = (str(i+1), self.lines[i][1])

    # Creates a new button
    def add_button(self, text, icon_path=None, target=None, tooltip_text=None):
        # Create new button and setup fonts and color
        new_button = QtWidgets.QPushButton(self.FileViewer)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        new_button.setFont(font)
        new_button.setStyleSheet("color: rgb(255, 255, 255);")

        # Set up icon
        if icon_path is not None:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            new_button.setIcon(icon)
            new_button.setIconSize(QtCore.QSize(32, 32))
            new_button.setObjectName("button")

        # Add tooltip
        if tooltip_text is not None:
            new_button.setToolTip("<span style=\"color:black;\">{}</span>".format(tooltip_text))

        # Set the text and attach button to the interface
        self.buttons.append(new_button)
        self.button_pane.addWidget(self.buttons[-1])
        self.buttons[-1].setText(text)

        # Set target
        if target is not None:
            self.buttons[-1].clicked.connect(target)

    # Adds a new line to the text window
    def add_line(self, line_num, text, prefix_spaces=5, suffix_spaces=0, highlighting='monokai'):
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
        highlighted_text = highlight_text(text + ''.join([' ' for i in range(suffix_spaces)]), highlighting)
        label_text = (_LINE_PRESERVE_PFX + str(line_num)
                     + _LINE_INDENT + ''.join([' ' for i in range(prefix_spaces - num_digits)])
                     + highlighted_text  # Add ending padding if specified
                     + _LINE_PRESERVE_SFX)
        text_label.setText(label_text)
        text_label.setStyleSheet("color: rgb(255, 255, 255);\nbackground-color: rgba(255, 255, 255, 0);")
        self.text_labels.append(text_label)
        self.text_area.addWidget(self.text_labels[-1])
        self.text_labels[-1].lower() # Send to the "back" so that things can be drawn on top of this label

    # Clear all lines from the text window
    def clear_lines(self):
        for i in reversed(range(self.text_area.count())): 
            self.text_area.itemAt(i).widget().setParent(None)
        self.text_labels = [] # Reset the internal labels array

    # Analyzes the selected file and populates the array of 'suggestions'
    def analyze(self):
        self.suggestions = []
        self.suggestion_infos = [] # Dialog boxes with info about suggestions
        self.fix_infos = []        # Dialog boxes with info about fixes

        # Get suggestions from the thesis program
        diag_title = 'Analyzing..'
        diag_text = 'Analyzing program.\nThis may take a few moments..'
        x = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).x() - 150 # Anchor dialog to center of window
        y = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).y() - 100
        diag = create_simple_dialog(self.scrollAreaWidgetContents, diag_title, diag_text, x, y, button=False)
        diag.show()
        lines = [x[1] for x in self.lines]
        source = ''.join(['{}\n'.format(line) if len(line) > 0 and line[-1] != '\n' else line for line in lines])
        suggestions = generate_suggestions(source, debug=False, slow=True, noprogress=True)
        diag.close

        # Nothing to suggest! Show dialog
        if len(suggestions) == 0:
            diag_title = 'Earthworm'
            diag_text = 'Nothing to suggest!'
            x = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).x() - 125 # Anchor dialog to center of window
            y = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).y() - 100
            diag = create_simple_dialog(self.scrollAreaWidgetContents, diag_title, diag_text, x, y, button=True)
            diag.exec_()
            return
        
        # Parse and turn into suggestion objects
        for s in suggestions:
            s_split = str(s).splitlines()

            # Get data from the suggestion
            start = int(s_split[0].split()[1].split('-')[0])
            end = int(s_split[0].split()[1].split('-')[1])
            function = s_split[0].split()[2][1:-2]
            i = start - 1
            lines = []
            while i != end:
                lines.append(self.lines[i])
                i += 1
            params = None
            returns = None

            # Get params and return values
            for i in range(1, len(s_split)):
                if 'parameters' in s_split[i]: # Getting parameters
                    params = s_split[i].replace(',', '').split()[1:]
                elif 'returns' in s_split[i]: # Getting return values
                    returns = s_split[i].replace(',', '').split()[1:]
                else: # Must be the reason
                    reason = s_split[i].replace('reason: ', '').lstrip()

            # Create suggestion object and insert it into the array
            suggestion = Suggestion(start, end, function, lines, reason, params=params, returns=returns)
            self.suggestions.append(suggestion)

        # Rearrange suggestions based on line numbers
        self.suggestions = list(sorted(self.suggestions, key=lambda s: s.start))
        self.update_suggestion_indices() # Renumber the suggestions

        # Before updating, clear any data from previous analyze
        self.scrollAreaWidgetContents.reset_state()

        # Set state after analyze
        self.scrollAreaWidgetContents.suggestions = self.suggestions
        self.scrollAreaWidgetContents.text_labels = self.text_labels
        self.scrollAreaWidgetContents.coords = self.scrollAreaWidgetContents.get_suggestion_coords()
        self.scrollAreaWidgetContents.colors = self.scrollAreaWidgetContents.get_colors(self.suggestions) # Pick colors for the suggestions
        self.scrollAreaWidgetContents.has_analyzed = True
        self.create_fix_infos() # Create the info dialogs
        self.create_suggestion_infos() # Create the info dialogs
        
        # Add new checkboxes and buttons
        for i in range(len(self.scrollAreaWidgetContents.coords)):
            (x, y, _, _) = self.scrollAreaWidgetContents.coords[i]
            # Set up info dialog
            diag_title = 'Earthworm'
            diag_text = 'Test'
            diag_x = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).x() - 125 # Anchor dialog to center of window
            diag_y = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).y() - 100
            diag = create_simple_dialog(self.scrollAreaWidgetContents, diag_title, diag_text, diag_x, diag_y, button=True)
            self.scrollAreaWidgetContents.dialogs.append(diag)

            # Add checkbox and button
            labels = self.text_labels[self.suggestions[i].start - 1 : self.suggestions[i].end]
            #self.scrollAreaWidgetContents.add_checkbox(x+3, y)
            self.scrollAreaWidgetContents.add_info_button(x+3, y+2, target=self.suggestion_infos[i].exec_)

        # Reset and repopulate lines with new spaces to account for drawn boxes
        self.populate_lines(self.lines, prefix_spaces=self.get_pfx_spaces(), suffix_spaces=25)
        self.scrollAreaWidgetContents.update()

        # Show results
        diag_title = 'Earthworm'
        diag_text = 'Analysis complete!\nEarthworm found {} issues.'.format(len(self.suggestions))
        x = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).x() - 250 # Anchor dialog to center of window
        y = self.scrollArea.mapToGlobal(self.scrollArea.rect().center()).y() - 100
        diag = create_simple_dialog(self.scrollAreaWidgetContents, diag_title, diag_text, x, y, button=True)
        diag.exec_()

    # Returns a Suggestion Info pane
    def get_suggestion_info(self, suggestion, fix_info):
        dialog = QtWidgets.QDialog()
        dialog.ui = SuggestionInfo(suggestion)
        dialog.ui.parent = self.FileViewer
        dialog.ui.child = fix_info
        dialog.ui.child.ui.parent = dialog # Establish links between parent and child
        dialog.ui.setupUi(dialog)
        return dialog

    # Returns a Fix Info pane
    def get_fix_info(self, suggestion):
        dialog = QtWidgets.QDialog()
        dialog.ui = FixInfo(suggestion)
        dialog.ui.setupUi(dialog)
        dialog.ui.populate_text()
        return dialog

    def create_suggestion_infos(self):
        self.suggestion_infos = []
        for i in range(len(self.suggestions)):
            # Use the original lines so that we can use the original spacing(s)
            st = self.suggestions[i].start
            end = self.suggestions[i].end
            self.suggestions[i].lines = self.lines[st - 1:end]
            si = self.get_suggestion_info(self.suggestions[i], self.fix_infos[i])

            # Hook up buttons
            si.ui.button_ok.clicked.connect(si.reject)
            si.ui.button_fix.clicked.connect(self.fix_infos[i].exec_)
            self.suggestion_infos.append(si)

    def create_fix_infos(self):
        self.fix_infos = []
        for i in range(len(self.suggestions)):
            # Use the original lines so that we can use the original spacing(s)
            st = self.suggestions[i].start
            end = self.suggestions[i].end
            self.suggestions[i].lines = self.lines[st - 1:end]
            fi = self.get_fix_info(self.suggestions[i])

            # Hook up buttons
            fi.ui.button_go.clicked.connect(fi.ui.custom_accept)
            fi.ui.button_cancel.clicked.connect(fi.reject)
            self.fix_infos.append(fi)


    # Returns the number of spaces to indent each line by
    # depending on the furthest x-coordinate of the drawn boxes
    def get_pfx_spaces(self):
        max_x = 0
        for (x, _, _, _) in self.scrollAreaWidgetContents.coords:
            if x > max_x:
                max_x = x

        return max_x // 40 * 5

    # Removes the path from the file, so only the filename.extension is left
    def truncate_filename(self):
        if '/' not in self.filename:
            return self.filename
        i = -1
        while self.filename[i] != '/':
            i -= 1
        return self.filename[i+1:]

    def retranslateUi(self, FileViewer):
        _translate = QtCore.QCoreApplication.translate
        self.set_window_title('Earthworm (' + self.truncate_filename() + ')')
