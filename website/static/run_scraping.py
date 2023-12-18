from website.static.programs import get_program, run_program

def run_script():
    list_program = get_program()
    for program in list_program:
        execute_program = run_program(program)