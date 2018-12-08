from cursesmenu import *
from cursesmenu.items import *
from CSP import CSP

csp = CSP()

def load_from_json():

	print("Enter the file name to laod csp from : ")
	filename = input()
	csp.load_from_json(filename)

def export_to_json():

	print("Enter the file name to export csp to : ")
	filename = input()
	csp.export_to_json(filename)
	
def solve():

	csp.backtrack_search()
	print("SOLVED !!")
	input()

def choose_mrv():

	csp.heuristic = "mrv"

def choose_dh():

	csp.heuristic = "dh"

def choose_first():

	csp.heuristic = "first"

def choose_random():

	csp.heuristic = "random"

def add_variable():

	variable = input("Choose a name for your variable : ")
	str_domain = input("Enter your variable's domain (space separated values) : ")
	domain = str_domain.split(' ')
	domain = [int(v) for v in domain]
	csp.add_variable(variable, domain)

def add_constraint():
	
	x, y = input("Enter the scope of your rule : ").split(' ')
	rule = input("Enter your rule : ")
	print(x," -> ", y)
	print(rule)
	input()
	csp.add_constraint(x, y, rule)

menu = CursesMenu("CSP Solver", "A CSP Solver engine")

add_variable_item = FunctionItem("Add a variable to CSP", add_variable)
add_constraint_item = FunctionItem("Add a constraint to CSP", add_constraint)
load_from_json_item = FunctionItem("Load CSP from JSON", load_from_json)
export_to_json_item = FunctionItem("Export CSP to JSON", export_to_json)

heuristics_menu = CursesMenu("Choose your heuristics : ")

choose_mrv_item = FunctionItem("Minimum Restraining Value", choose_mrv)
choose_dh_item = FunctionItem("Degree Heuristic", choose_dh)
choose_first_item = FunctionItem("First", choose_first)
choose_random_item = FunctionItem("Random", choose_random)


heuristics_menu.append_item(choose_mrv_item)
heuristics_menu.append_item(choose_dh_item)
heuristics_menu.append_item(choose_random_item)
heuristics_menu.append_item(choose_first_item)

choose_heuristics_menu = SubmenuItem("Choose heuristics",heuristics_menu, menu)

solve_item = FunctionItem("Solve CSP", solve)

menu.append_item(add_variable_item)
menu.append_item(add_constraint_item)
menu.append_item(choose_heuristics_menu)
menu.append_item(load_from_json_item)
menu.append_item(export_to_json_item)
menu.append_item(solve_item)

if __name__ == "__main__":

	menu.show()
