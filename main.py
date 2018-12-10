from cursesmenu import *
from cursesmenu.items import *
from CSP import CSP

csp = CSP()

def load_from_json():

	print("Enter the file name to load csp from : ")
	filename = input()
	csp.load_from_json(filename)

def export_to_json():

	print("Enter the file name to export csp to : ")
	filename = input()
	csp.export_to_json(filename)
	
def generate_single():

	csp.all_solutions = False
	if csp.is_solved():
		print("CSP already solved")
	else:
		csp.solve()
		print("SOLVED !!")
	input()

def generate_all():

	csp.all_solutions = True
	if csp.is_solved():
		print("CSP already solved")
	else:
		csp.solve()
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


def select_ac3():

	csp.algorithm = "ac3"


def select_fc():

	csp.algorithm = "fc"


def select_bt():

	csp.algorithm = "bt"

def select_lcs():

	csp.order_value = "lcs"

def select_none():

	csp.order_value = None

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

def choose_log_file():

	filename = input("Enter Log file name (default=trace.log) : ")
	if filename != "":
		csp.log = open(filename, "w")

def save():

	filename = input("Enter file to save solution in (default=solutions.json): ")
	if filename != "":
		csp.save_solution(filename)
	else:
		csp.save_solution()
	input()

def display_solution():

    scriptname = input("Enter solution renderer : ")
    exec(open(scriptname).read())

menu = CursesMenu("CSP Solver", "A CSP Solver engine")

algorithm_menu = CursesMenu("Algorithm", "Select the algorithm to solve CSP with : ")

algorithm_ac3_item = FunctionItem("Arc Consistency 3", select_ac3)
algorithm_fc_item = FunctionItem("Forward Checking", select_fc)
algorithm_bt_item = FunctionItem("Backtracking", select_bt)

algorithm_menu.append_item(algorithm_ac3_item)
algorithm_menu.append_item(algorithm_fc_item)
algorithm_menu.append_item(algorithm_bt_item)
algorithm_item = SubmenuItem("Choose algorithm", algorithm_menu, menu)

order_value_menu = CursesMenu("Value Ordering", "Order values by : ")

order_value_lcs_item = FunctionItem("Least Constraining Values", select_lcs)
order_value_none_item = FunctionItem("None", select_none)

order_value_menu.append_item(order_value_lcs_item)
order_value_menu.append_item(order_value_none_item)

order_value_item = SubmenuItem("Choose how to order values", order_value_menu, menu)

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

log_item = FunctionItem("Choose Log file", choose_log_file)


solve_menu = CursesMenu("Solve CSP")

generate_single_item = FunctionItem("Generate single solution", generate_single)
generate_all_item = FunctionItem("Generate all solutions", generate_all)

solve_menu.append_item(generate_single_item)
solve_menu.append_item(generate_all_item)

solve_item = SubmenuItem("Solve CSP", solve_menu, menu)
save_item = FunctionItem("Save found solution(s)", save)

display_solution_item = FunctionItem("Display Solution", display_solution)

menu.append_item(add_variable_item)
menu.append_item(add_constraint_item)
menu.append_item(choose_heuristics_menu)
menu.append_item(algorithm_item)
menu.append_item(order_value_item)
menu.append_item(log_item)
menu.append_item(load_from_json_item)
menu.append_item(export_to_json_item)
menu.append_item(solve_item)
menu.append_item(display_solution_item)
menu.append_item(save_item)

if __name__ == "__main__":

	menu.show()

