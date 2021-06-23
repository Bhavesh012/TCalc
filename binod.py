def magnification(t_focal,o_focal):
    """Calculates Magnification for the telescope

    Args:
        t_focal(float): Focal Length of the Telescope
        o_focal(float): Ocular Focal Length

    Returns:
        float: Magnification of the telescope

    """
    return t_focal/o_focal




def true_fov(o_diameter,t_focal_length):
    """Calulate the True Field of View

    Args:
    o_diameter(float): Ocular field stop diameter
    t_focal_length(float): Telescope focal length

    Returns:
        float: True Field of View
    
    """
    return o_diameter/t_focal_length*57.3