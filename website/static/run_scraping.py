from website.static.programs import get_program, run_program

def run_script(file_name):
    list_program = get_program()
    for program in list_program:
        if file_name in program:
            execute_program = run_program(file_name)