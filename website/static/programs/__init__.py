import os
from website.static.programs.shopping_apparel_abahouse import ShoppingApparelAbahouse
from website.static.programs.shopping_apparel_adabat import ShoppingApparelAdabat
from website.static.programs.shopping_apparel_adametrope import ShoppingApparelAdametrope
from website.static.programs.shopping_apparel_anteprima import ShoppingApparelAnteprima
from website.static.programs.shopping_apparel_bape import ShoppingApparelBape

def get_program():
    list_program = [x for x in os.listdir('website/static/programs') if '__' not in x and x.endswith('.py')]
    print(list_program)

    return list_program

def run_program(file_name):
    if 'shopping_apparel_abahouse' in file_name:
        ShoppingApparelAbahouse()
    if 'shopping_apparel_adabat' in file_name:
        ShoppingApparelAdabat()
    if 'shopping_apparel_adametrope' in file_name:
        ShoppingApparelAdametrope()
    if 'shopping_apparel_anteprima' in file_name:
        ShoppingApparelAnteprima()
    if 'shopping_apparel_bape' in file_name:
        ShoppingApparelBape()