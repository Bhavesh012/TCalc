def age_to_eye_diameter(age):
    """Calulates the size of an eye given an age 

    Args:
         age (float): age of the observer
    Returns:
         D_eye (float): Best diameter of Eyepiece (mm)    
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

    return D_eye

def eye_to_age(D_eye):
    """Inverts age_to_eye_diameter 

    Args:
         D_eye (float): Diameter of Eyepiece (mm); default is 7 mm
    Returns:
         age (float): approximate age
    """ 

    if D_eye > 7.25:
        age = 15
    elif D_eye <= 7.25 and D_eye > 6.75:
        age = 25
    elif D_eye <= 6.75 and D_eye > 6.25:
        age = 33
    elif D_eye <= 6.25 and D_eye > 5.75:
        age = 40
    elif D_eye <= 5.75 and D_eye > 5.25:
        age = 54
    else:
        age = 70

    return age
