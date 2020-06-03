# Class representing a Suggestion offered by Earthworm
class Suggestion:
    def __init__(self, start, end, function, lines, reasons, index=0, params=None, returns=None):
        self.start = start         # Starting line number
        self.end = end             # Ending line number
        self.function = function   # The function this suggestion came from
        self.lines = lines         # The text this suggestion is comprised of
        self.params = params       # The suggested params for the new function
        self.returns = returns     # The name of the return variable for the new function
        self.reasons = self.format_reasons(reasons)  # Earthworm's given reason(s) for this suggestion
        self.index = index         # Which suggestion this is

    def format_reasons(self, reasons):
        i = 1
        r = []
        seen = []
        for s in reasons.split('.'):
            s = s.lstrip() # Remove preceeding whitespace
            if s == '' or s in seen:
                continue
            seen.append(s)
            r.append('{}. {}.\n'.format(i, s))
            i += 1
        return r # set() removes duplicates

    # Shifts this suggestion up or down. Updates start and end points as well as line numbers
    def shift_lines(self, direction='up', count=0):
        if direction == 'down': # Shifting down
            self.start = self.start + count
            self.end = self.end + count
            for j in range(len(self.lines)):
                (lineno, content) = self.lines[j]
                self.lines[j] = (str(int(lineno) + count), content)
        else: # Shifting up
            self.start = self.start - count
            self.end = self.end - count
            for j in range(len(self.lines)):
                (lineno, content) = self.lines[j]
                self.lines[j] = (str(int(lineno) - count), content)

    def __str__(self):
        s = '<Suggestion>\n'
        s += 'start: {}\n'.format(self.start)
        s += 'end: {}\n'.format(self.end)
        s += 'function: {}\n'.format(self.function)
        s += 'lines:\n'
        for i in range(len(self.lines)):
            s += '    {}. {}'.format(self.lines[i][0], self.lines[i][1])
        s += 'params: {}\n'.format(self.params)
        s += 'returns: {}\n'.format(self.returns)
        s += 'reasons:\n'
        for r in self.reasons:
            s += '    {}\n'.format(r)
        return s
        