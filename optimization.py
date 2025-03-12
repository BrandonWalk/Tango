from pulp import LpProblem, LpVariable, value

problem = LpProblem("Tango")

# declare decision variables

rows = []
for r in range(6):
    column = []
    for c in range(6):
        column.append(LpVariable(f"var_{r}_{c}", cat="Binary"))
    rows.append(column)

# basic constraints

for row in rows:
    problem += sum(row) == 3

for column in range(6):
    problem += sum([row[column] for row in rows]) == 3

for row in rows:
    problem += sum(row[0:3]) <= 2
    problem += sum(row[0:3]) >= 1
    problem += sum(row[1:4]) <= 2
    problem += sum(row[1:4]) >= 1
    problem += sum(row[2:5]) <= 2
    problem += sum(row[2:5]) >= 1
    problem += sum(row[3:6]) <= 2
    problem += sum(row[3:6]) >= 1

for column_index in range(6):
    column_list = [row[column_index] for row in rows]
    problem += sum(column_list[0:3]) <= 2
    problem += sum(column_list[0:3]) >= 1
    problem += sum(column_list[1:4]) <= 2
    problem += sum(column_list[1:4]) >= 1
    problem += sum(column_list[2:5]) <= 2
    problem += sum(column_list[2:5]) >= 1
    problem += sum(column_list[3:6]) <= 2
    problem += sum(column_list[3:6]) >= 1

# individual game constraints

from bs4 import BeautifulSoup
soup = BeautifulSoup(open("game3.html"))

for cell_number, cell in enumerate(soup.find_all("div", {"class": "lotka-cell"})):
    divs = cell.find_all("div")
    # convert cell number into row and column numbers
    r = cell_number//6
    c = cell_number % 6
    for div in divs:
        if "lotka-cell-content" in div["class"]:
            icons = div.find_all("svg")
            for icon in icons:
                if icon["aria-label"] == "Moon":
                    # cell must have a moon
                    problem += rows[r][c] == 1
                elif icon["aria-label"] == "Sun":
                    # cell must have a sun
                    problem += rows[r][c] == 0
        elif "lotka-cell-edge--right" in div["class"]:
            icons = div.find_all("svg")
            for icon in icons:
                if icon["aria-label"] == "Cross":
                    # cell must be different from the cell to the right
                    problem += rows[r][c] != rows[r][c+1]
                elif icon["aria-label"] == "Equal":
                    # cell must be the same as the cell to the right
                    problem += rows[r][c] == rows[r][c+1]
        elif "lotka-cell-edge--bottom" in div["class"]:
            for icon in icons:
                if icon["aria-label"] == "Cross":
                    # cell must be different from the cell in the row below
                    problem += rows[r][c] != rows[r+1][c]
                elif icon["aria-label"] == "Equal":
                    # cell must be the same as the cell in the row below
                    problem += rows[r][c] == rows[r+1][c]

# solve

problem.solve()

# print solution

for r in range(6):
    for c in range(6):
        print(int(value(rows[r][c])), end="")
    print("")
