from TCalc.tcalc import eyepiece, telescope

piece1 = eyepiece(5, 50)
piece2 = eyepiece(1, 50)

my_telescope = telescope(50,300)

my_telescope.add_eyepiece(piece1)
my_telescope.add_eyepiece(piece2)
my_telescope.add_eyepiece(piece1,'copy of 1',select=False)

my_telescope.list_eyepiece()

my_telescope.say_configuration()

my_telescope.select_eyepiece(0)
my_telescope.say_configuration()

my_telescope.show_resolving_power()
my_telescope.show_magnification_limits()
my_telescope.show_eyepiece_limits()
