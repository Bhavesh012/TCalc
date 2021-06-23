#creating telescope class
# D_o = dia of aperture
# D_e = dia of eyepiece
# D_EP = dia of exit pupil = (D_o*f_e)/(f_o + f_e) = D_o/(M+1) ~ D_o/M = f_e/f_R
# W = wavelength of light
# f_o = focal length of objective
# f_e = focal length of eyepiece
# f_R = focal ratio = f_o/D_o = f_e_min (eyepiece for M_max)
# M = visual magnification = f_o/f_e
# M_max = max. magnification = aprrox. 2*D_o x
# M_min = min. magnification = D_o/D_eye (D_eye = 7mm generally)
# P_R = Resolving Power = 1.22*W/D_o (in Radians) = 251661600*W/D_o(mm) (arc-sec)
# Dawes_lim = Dawes Limit = 4.56 arc-sec/D_o(in) = 115.8/D_o(mm)
# Image Resolution = 120/M
# fov_e = FOV of eyepiece (generally 52 deg)
# fov_scope = FOV of scope = fov_e/M
# afov = Apparent FOV
# fov = True FOV = afov/M = (ocular field stop dia/f_e)*57.3
# Lmag_limit = Limiting Mag of Telescope = 2 + 5*np.log(D_o)
# SB = Surface Brightness = 2*(D_EP**2) (in %)

# PPI = Power per inch = M/D_o(in)

# Barlow = 2*f_o
# Reducer = P_reducer*f_o

# exit pupil of about 2-3mm (2.4mm to be precise) is the optimum point for maximizing the resolving power of the eye
# Maximum Brightness	        D_EP = 7mm
# Half-Maximum Brightness	    D_EP = 5mm
# Half-Maximum Magnification	D_EP = 2mm
# Maximum Magnification	        D_EP = 1mm
# Extra-High Magnification	    D_EP = 2/3mm

# f_e_min = The min. focal length of eyepiece you can use => f_o/f_e_min = M_max
# f_e_max = The max. focal length of eyepiece you can use => pupil diameter*f_R

# Age (years)	Pupil Size (mm)
# 20 or less	7.5
# 30	        7.0
# 35	        6.5
# 45	        6.0
# 60	        5.5
# 80	        5.0

import numpy as np
import astropy.units as u 

class telescope():
    def __init__(self, D_o, f_o, ):
        self.aperture = D_o*u.mm
        self.f_o = f_o*u.mm