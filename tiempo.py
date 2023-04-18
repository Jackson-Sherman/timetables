import re

class mytime:
    _valid_regex = re.compile("(1?[0-9]):([0-5][0-9]) ([AP])M")
    def __init__(self, time_string):
        match = mytime._valid_regex.match(time_string)
        assert match is not None

        self.str = time_string

        hstr, mstr, aorp = match.groups()

        self.val = 12 if aorp == 'P' else 0
        hrs = int(hstr)
        mins = int(mstr)

        hrs %= 12

        self.val += hrs
        self.val *= 60
        self.val += mins
    
    def __lt__(self, other): return self.val < other.val
    def __le__(self, other): return self.val <= other.val
    def __eq__(self, other): return self.val == other.val
    def __ne__(self, other): return self.val != other.val
    def __gt__(self, other): return self.val > other.val
    def __ge__(self, other): return self.val >= other.val

    def __str__(self): return self.str
