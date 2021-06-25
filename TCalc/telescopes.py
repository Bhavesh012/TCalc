from tcalc import telescope, eyepiece

# Create a Celestron Nexstar 8SE
celestron_nexstar_8se = telescope(D_o=203.2,f_o=2032)
lens1 = eyepiece(f_e=25)
celestron_nexstar_8se.add_eyepiece(lens1,id='included eyepiece')

celestron_nexstar_8se.say_configuration()