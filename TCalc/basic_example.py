  
from TCalc.tcalc import barlow_lens, eyepiece, focal_reducer, telescope

piece1 = eyepiece(5, 50)
piece2 = eyepiece(1, 50)
reducer = focal_reducer(.5)
barlow = barlow_lens() # Default factor is 2

my_telescope = telescope(50,300)

my_telescope.add_eyepiece(piece1,select=True)
my_telescope.add_eyepiece(piece2,select=True)
my_telescope.add_eyepiece(piece1,'copy of 1',select=False)

my_telescope.add_optic(reducer,'reducer 1', select=False)
my_telescope.add_optic(barlow,'barlow 1', select=True)

my_telescope.list_eyepiece()

my_telescope.say_configuration()

my_telescope.select_eyepiece(0)
my_telescope.select_optic(None)
my_telescope.say_configuration()

my_telescope.show_resolving_power()
my_telescope.show_magnification_limits()
my_telescope.show_eyepiece_limits()
