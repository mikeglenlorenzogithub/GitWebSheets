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

def run_program(list_program):
    if 'shopping_apparel_abahouse.py' in list_program:
        ShoppingApparelAbahouse()
    if 'shopping_apparel_adabat.py' in list_program:
        ShoppingApparelAdabat()
    if 'shopping_apparel_adametrope.py' in list_program:
        ShoppingApparelAdametrope()
    if 'shopping_apparel_anteprima.py' in list_program:
        ShoppingApparelAnteprima()
    if 'shopping_apparel_bape.py' in list_program:
        ShoppingApparelBape()