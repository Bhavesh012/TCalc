from tcalc import telescope, eyepiece

# Create a Celestron NexStar 8SE preset
celestron_nexstar_8se = telescope(D_o=203.2,f_o=2032)
omni_25 = eyepiece(f_e=25)
celestron_nexstar_8se.add_eyepiece(omni_25,id='Omni 25mm eyepiece')

celestron_nexstar_8se.say_configuration()