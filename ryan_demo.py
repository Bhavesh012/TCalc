from ryan_telescope import eyepiece, telescope

piece1 = eyepiece(5, 50)
piece2 = eyepiece(1, 50)

my_telescope = telescope(50,1000)

my_telescope.list_eyepiece()

my_telescope.add_eyepiece(piece1)
my_telescope.add_eyepiece(piece2)
my_telescope.add_eyepiece(piece1,'copy of 1',select=False)

my_telescope.list_eyepiece()

print(my_telescope.magnification)
my_telescope.select_eyepiece(0)
print(my_telescope.magnification)
