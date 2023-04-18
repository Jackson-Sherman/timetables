day_type = "10-7" # either "10-10" or "10-7"
fp = "from_shift_swap.txt" # or name of txt file in your folder

class Shift:
    DEFAULT = "10-10"
    day_type = (DEFAULT,"10-7")[1]
    shift_names = ('ad','o','os','opos','s','cpos','sc','c','error')

    def __init__(self, name, start=None, end=None, typ=DEFAULT):
        if start is None and end is None:
            name = str(name)
            name, start, _, end = name.splitlines()
        self._typ = typ

        assert isinstance(name, str) and isinstance(start, str) and isinstance(end, str)

        self._name = name if name[-1] != '\n' else name[:-1]

        def get_int(line):
            return int(line[0] if line[1] == ':' else line[:2])

        self._start = get_int(start)
        self._end = get_int(end)
    
    def _split_name(st):
        last,rest = st.split(", ")
        first = rest[:-2] if rest[-2] == ' ' else rest
        return first, last

    def split_name(self):
        return Shift._split_name(self._name)

    def _present_name(st):
        return "{:12} {:12}".format(*Shift._split_name(st))

    def present_name(self):
        return Shift._present_name(self._name)

    def get_name(self,pretty=True):
        return self.present_name() if pretty else self._name
    
    def all_day(self):
        return {
            Shift.DEFAULT: self._start in {7,8,9,10} and self._end in {10,11,12,1},
            "10-7": self._start in {8,9,10} and self._end in {7,8,9},
        }[self._typ]

    def open(self):
        return {
            Shift.DEFAULT: self._start in {7,8,9,10} and self._end in {4,5},
            "10-7": self._start in {8,9,10} and self._end in {4,5,6},
        }[self._typ]

    def open_swing(self):
        return {
            Shift.DEFAULT: self._start in {7,8,9,10} and self._end in {7,8,9},
            "10-7": False,
        }[self._typ]

    def open_po_swing(self):
        return {
            Shift.DEFAULT: self._start in {11,12}    and self._end in {4,5},
            "10-7": self._start in {8,9,10} and self._end in {4,5,6},
        }[self._typ]

    def swing(self):
        return {
            Shift.DEFAULT: self._start in {11,12}    and self._end in {7,8,9},
            "10-7": False,
        }[self._typ]

    def close_po_swing(self):
        return {
            Shift.DEFAULT: self._start in {3,4,5}    and self._end in {7,8},
            "10-7": False,
        }[self._typ]

    def swing_close(self):
        return {
            Shift.DEFAULT: self._start in {11,12}    and self._end in {9,10,11,12,1},
            "10-7": self._start in {11,12} and self._end in {7,8,9},
        }[self._typ]

    def close(self):
        return {
            Shift.DEFAULT: self._start in {3,4,5}    and self._end in {9,10,11,12,1},
            "10-7": self._start in {2,3,4} and self._end in {7,8,9},
        }[self._typ]

    def get_shift_dict(shifts):
        dic = {sn: () for sn in Shift.shift_names}
        for person in shifts:
            assert isinstance(person, Shift)
            if person.all_day():
                dic['ad'] += (person,)
            elif person.open():
                dic['o'] += (person,)
            elif person.open_swing():
                dic['os'] += (person,)
            elif person.open_po_swing():
                dic['opos'] += (person,)
            elif person.swing():
                dic['s'] += (person,)
            elif person.close_po_swing():
                dic['cpos'] += (person,)
            elif person.swing_close():
                dic['sc'] += (person,)
            elif person.close():
                dic['c'] += (person,)
            else:
                dic['error'] += (person,)
        return dic

    def print_shifts(shifts, show_count=False, name_form_str=None):
        dic = Shift.get_shift_dict(shifts)
        for sn in Shift.shift_names:
            if dic[sn]:
                if show_count:
                    print(sn.upper() + " x" + str(len(dic[sn])))
                print('=' * 10)
                for person in dic[sn]:
                    print(person.present_name() if name_form_str is None else name_form_str.format(*person.split_name()))
                print()
    
    def print_table_header():
        print(" "*25 + " O  So Sc C ")
    
    def print_table_row(self):
        output = None
        if self.all_day():          output = (1,1,1,1)
        elif self.open():           output = (1,1,0,0)
        elif self.open_swing():     output = (1,1,1,0)
        elif self.open_po_swing():  output = (0,1,0,0)
        elif self.swing():          output = (0,1,1,0)
        elif self.close_po_swing(): output = (0,0,1,0)
        elif self.swing_close():    output = (0,1,1,1)
        elif self.close():          output = (0,0,1,1)
        else:                       output = (2,2,2,2)
        def tup2st(tup):
            otpt = ""
            for v in tup:
                otpt += ' ' + ('X' if v == 1 else ' ' if v == 0 else '?') + ' '
            return otpt
        print(self.present_name() + tup2st(output))
        return output
    
    def print_table(shifts):
        Shift.print_table_header()
        dic = Shift.get_shift_dict(shifts)
        output = [0,0,0,0]
        for sn in Shift.shift_names:
            if dic[sn]:
                for person in dic[sn]:
                    vals = person.print_table_row()
                    for i in range(4):
                        output[i] += 1 if vals[i] == 1 else 0
        print(("{:24}" + "{:>3}"*4).format("Total",*output))
        return output
        

def get_shifts(type_of_day="10-10", fp="from_shift_swap.txt"):
    with open(fp,"r") as file:
        lines = file.read().splitlines()

    shifts = []
    for i in range(0,len(lines),4):
        start,end = lines[i].split(" - ")
        if end[-9] == ' ':
            end = end[:-9]
        elif end[-10] == ' ':
            end = end[:-10]
        else:
            assert False
        name = lines[i+3][1:]
        shifts.append(Shift(name, start, end, type_of_day))
    return shifts

if __name__ == "__main__":
    s = get_shifts(day_type)
    Shift.print_shifts(s, True)
    Shift.print_table(s)