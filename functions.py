import numpy as np
import astropy.units as u 


def magnification(f_o,f_e):
    """Calculates the Angular Magnification for the telescope

    Args:
        f_o(float): Focal Length of Objective/Aperture (mm)
        f_e(float): Focal Length of Eyepiece (mm)

    Returns:
        float: Visual Magnification (M) of the telescope

    """
    return f_o/f_e


def focal_ratio(f_o,D_o):
    """Calculates the Focal Ratio for the telescope

    Args:
        f_o(float): Focal Length of Objective/Aperture (mm)
        D_o(float): Diameter of Objective/Aperture (mm)

    Returns:
        float: Focal Ratio/f-number (:math: `f_R`) of the telescope

    """
    return f_o/D_o


def true_fov(M, fov_e=50):
    """Calulates the True Field of View (FOV) of the telescope & eyepiece pair 

    Args:
        fov_e (float): FOV of eyepiece; default 50 deg
        M (float): Magnification of Telescope

    Returns:
        float: True Field of View (deg)
    
    """
    return fov_e/M

def exit_pupil(f_e,f_R):
    """Calulates the Exit Pupil of the telescope & eyepiece pair 

    Args:
        f_e (float): Focal Length of eyepiece (mm)
        f_R (float): Focal Ratio of telescope

    Returns:
        float: Diameter of Exit Pupil(:math: `D_EP`) (mm)
    
    Note:
        For optimal usage, :math: `D_EP \approx 2-3 mm` is the optimum range for maximizing the resolving power of the eye

    """
    return f_e/f_R

def resolving_power(W,D_o):
    """Calulates the Reosultion of the telescope
    
    Args:
        W (float): Wavelength of light recieved (nm)
        D_o (float): Diameter of Objective/Aperture (mm)

    Returns:
        float: Resolving power of the telescope (:math: `P_R`) (arc-sec)
    
    Note: 
        This function is generally useful when you are using filters. For filter-less observations, check Dawes Limit function.

    """
    return 0.2516616*(W/D_o)

def dawes_lim(D_o):
    """Calulates the Reosultion of the telescope according to the Dawes Limit
    
    Args:
         D_o (float): Diameter of Objective/Aperture (mm)

    Returns:
        float: Resolving power of the telescope arroding to Dawes Limit (arc-sec)
    
    Note: 
        This function is generally useful when you are doing filter-less observations. For operation with filters, check Resolution Power function.

    """ 
    return 115.8/D_o

def Max_magnification(D_o):
    """Calulates the maximum usable magnification of the telescope 

    Args:
         D_o (float): Diameter of Objective/Aperture (mm)

    Returns:
        float: Maximum Usable Magnification (:math: `M_max`) of the telescope
    
    Note: 
        The maximum usable magnification also depends upon seeing.
    """ 
    return 2*D_o

def Min_magnification(D_o,D_eye=7,age=None):
    """Calulates the minimum usable magnification of the telescope 

    Args:
         D_o (float): Diameter of Objective/Aperture (mm)
         D_eye (float): Diameter of Eyepiece (mm); default is 7 mm
    Returns:
        float: Minimum Usable Magnification (:math: `M_min`) of the telescope
    
    """ 
    if age <= 20:
        D_eye = 7.5
    elif ((age> 20) and (age<= 30)):
        D_eye = 7
    elif ((age> 30) and (age<= 35)):
        D_eye = 6.5
    elif ((age> 35) and (age<= 45)):
        D_eye = 6
    elif ((age> 45) and (age<= 60)):
        D_eye = 5.5
    else: 
        D_eye = 5.0
 
    return D_o/D_eye

def Min_eyepiece(f_o,M_max):
    """Calulates the minimum focal length of eyepiece you can use on the telescope 

    Args:
         f_o (float): Focal length of Objective/Aperture (mm)
         M_max (float): Maximum usable magnification
    Returns:
        float: The minimum focal length of eyepiece (:math: `f_{e-min}`) you can use with your telescope 
    
    """ 
    return f_o/M_max

def Max_eyepiece(f_R, D_eye=7, age=None):
    """Calulates the maximum focal length of eyepiece you can use on the telescope 

    Args:
         D_eye (float): Diameter of Eyepiece (mm); default is 7 mm
         f_R (float): Focal Ratio/f-number of telescope
    Returns:
        float: The maximum focal length of eyepiece (:math: `f_{e-max}`) you can use with your telescope 
    
    """ 
    if age <= 20:
        D_eye = 7.5
    elif ((age> 20) and (age<= 30)):
        D_eye = 7
    elif ((age> 30) and (age<= 35)):
        D_eye = 6.5
    elif ((age> 35) and (age<= 45)):
        D_eye = 6
    elif ((age> 45) and (age<= 60)):
        D_eye = 5.5
    else: 
        D_eye = 5.0
 
    return f_R*D_eye    


def Lmag_limit(D_o):
    """Calculates the magnitude of the faintest star which can be seen from the telescope
    
    Args:
         D_o (float): Diameter of Objective/Aperture (mm)
    
    Returns:
        float: Limiting Magnitude (LM) of telescope 
    """
    return 2 + 5*np.log(D_o)

def surface_brightness(D_EP):
    """Calculates the surface brightness of the object as seen from the telescope
    
    Args:
         D_o (float): Diameter of Exit Pupil (mm)
    
    Returns:
        percentage: Surface Brightness (SB)
    """
    return 2*(D_EP**2) 

