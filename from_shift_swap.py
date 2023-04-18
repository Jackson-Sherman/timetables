from coworking_shifts import Shift

def get_shifts(fp="from_shift_swap.txt"):
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
        shifts.append(Shift(name, start, end))
    return shifts

s = get_shifts()
Shift.print_shifts(s, True)
Shift.print_table(s)

drivers = {
    "Mentel, AJ D",
    "Retherford, Kayleigh A",
    "Weeks, Josh C",
    "Sherman, Jackson J",
    "Middendorf, Cameron M",
    "Baker, Ryan C"
}
wont_show = {
    "Griswold, Ryan A",
    "Rosenblum, Ross",
    "Brake, Liam H"
}
soon_to_be = {
    "Griswold, Ryan A",
}

# with open("tempr.txt") as file:
#     lines = file.read().splitlines()
# for line in sorted(lines):
#     if True or line.split("] ")[1] not in wont_show:
#         print(line)