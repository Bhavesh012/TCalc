import numpy as np

from tcalc import barlow_lens, eyepiece, focal_reducer, telescope
from tcalc import age_list, eye_diameter_list, blue, green, red, wavelengths_list
from age_eye import age_to_eye_diameter, eye_to_age

def test_eyepiece_flength_violation():
    """Test invalid inputs for eyepiece flength"""

    flength = 0
    
    try:
        eyepiece(flength)
        raise ValueError("Invalid argument accepted")
    except:
        pass
    
    flength = -10
    
    try:
        eyepiece(flength)
        raise ValueError("Invalid argument accepted")
    except:
        pass

def test_eyepiece_fov_violation():
    """Test invalid inputs for eyepiece fov"""

    flength = 10
    fov = 0
    
    try:
        eyepiece(flength,fov)
        raise ValueError("Invalid argument accepted")
    except:
        pass
    
    flength = 10
    fov = -10
    
    try:
        eyepiece(flength,fov)
        raise ValueError("Invalid argument accepted")
    except:
        pass

def test_eyepiece_state():
    """Test eyepiece state is correctly preserved"""

    f_e = 10
    fov_e = 50
    
    test_eyepiece = eyepiece(f_e,fov_e)

    assert test_eyepiece.fov_e == fov_e
    assert test_eyepiece.f_e == f_e

def test_telescope_eyepiece_state():
    """Confirm eyepiece state is preserved when selecting 
    and deselecting on telescope"""
    
    f_e = 10
    fov_e = 50
    test_eyepiece = eyepiece(f_e,fov_e)

    D_o = 100
    f_o = 100
    test_tel = telescope(D_o, f_o, user_age=25)

    test_tel.add_eyepiece(test_eyepiece,select=True)

    assert test_tel.current_eyepiece.fov_e == fov_e
    assert test_tel.current_eyepiece.f_e == f_e

    assert test_tel.eyepieces['0'].fov_e == fov_e
    assert test_tel.eyepieces['0'].f_e == f_e

    test_tel.select_eyepiece()

    assert test_tel.current_eyepiece is None

    test_tel.select_eyepiece('0')

    assert test_tel.current_eyepiece.fov_e == fov_e
    assert test_tel.current_eyepiece.f_e == f_e

def test_telescope_invalid_inputs():
    """Test invalid inputs for telescope init"""

    D_o = 0
    f_o = 100
    
    try:
        telescope(D_o, f_o)
        raise ValueError("Invalid argument accepted")
    except:
        pass

    D_o = 100
    f_o = 0
    
    try:
        telescope(D_o, f_o)
        raise ValueError("Invalid argument accepted")
    except:
        pass

def test_telescope_age_inputs():
    """Different cases for age and user eye inputs"""

    D_o = 100
    f_o = 100
    
    test_tel = telescope(D_o, f_o)
    assert test_tel.user_age == 25
    assert test_tel.user_D_eye == age_to_eye_diameter(25)

    user_D_eye = 6
    user_age = 30

    test_tel = telescope(D_o, f_o, user_D_eye, user_age)
    assert test_tel.user_age == user_age
    assert test_tel.user_D_eye == user_D_eye

    user_D_eye = 6
    user_age = None

    test_tel = telescope(D_o, f_o, user_D_eye, user_age)
    assert test_tel.user_age is None
    assert test_tel.user_D_eye == user_D_eye

    user_D_eye = None
    user_age = 30

    test_tel = telescope(D_o, f_o, user_D_eye, user_age)
    assert test_tel.user_age == 30
    assert test_tel.user_D_eye == age_to_eye_diameter(user_age)


def assertions_for_tel_state(test_tel, f_o, D_o, D_eye):
    """Assertions with the raw calculations for various telescope properties"""
    
    assert test_tel.f_R == f_o/D_o
    assert test_tel.Dawes_lim == 115.8/D_o
    assert np.all(test_tel.P_R == 0.2516616*(wavelengths_list/D_o))
    assert test_tel.blue_P_R == 0.2516616*(blue/D_o)
    assert test_tel.green_P_R == 0.2516616*(green/D_o)
    assert test_tel.red_P_R == 0.2516616*(red/D_o)
    assert test_tel.M_min == D_o/D_eye
    assert np.all(test_tel.M_min_by_age == D_o/eye_diameter_list)
    assert test_tel.M_max == 2*D_o
    assert test_tel.f_e_min == f_o / (2*D_o)
    assert test_tel.f_e_max == (f_o/D_o) * D_eye
    assert np.all(test_tel.f_e_max_by_age == (f_o/D_o) * eye_diameter_list)
    assert np.isclose(test_tel.Lmag_limit, 2+5*np.log10(D_o),rtol=.01)


def test_telescope_tel_properties():
    """Make sure telescope initializes with correct properties"""

    D_o = 100
    f_o = 100
    D_eye = 7
    
    test_tel = telescope(D_o, f_o, D_eye)

    assertions_for_tel_state(test_tel, f_o, D_o, D_eye)

    assert np.isnan(test_tel.M)
    assert np.isnan(test_tel.fov)
    assert np.isnan(test_tel.D_EP)
    assert np.isnan(test_tel.SB)

def test_change_user_age():
    """Make sure telescope initializes with correct properties"""

    D_o = 100
    f_o = 100

    test_tel = telescope(D_o, f_o)
    D_eye0 = test_tel.user_D_eye
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye0)

    age = 10
    D_eye_new = age_to_eye_diameter(age)
    test_tel.change_user_age(age)
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye_new)

    age = 25
    D_eye_new = age_to_eye_diameter(age)
    test_tel.change_user_age(age)
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye_new)

    age = 70
    D_eye_new = age_to_eye_diameter(age)
    test_tel.change_user_age(age)
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye_new)

def assertions_for_eyepieces(test_tel, f_o, D_o, f_e, fov_e):
    assert test_tel.M == f_o/f_e
    assert test_tel.fov == fov_e/(f_o/f_e)
    assert test_tel.D_EP == f_e/(f_o/D_o)
    assert test_tel.SB == 2*(f_e/(f_o/D_o))**2

def test_telescope_add_eyepieces():
    """Test that changing lenses works correctly"""
    
    f_e1 = 10
    fov_e1 = 50
    test_eyepiece1 = eyepiece(f_e1,fov_e1)
    f_e2 = 20
    fov_e2 = 50
    test_eyepiece2 = eyepiece(f_e2,fov_e2)
    f_e3 = 30
    fov_e3 = 30
    test_eyepiece3 = eyepiece(f_e3,fov_e3)

    D_o = 100
    f_o = 100
    D_eye = 7
    test_tel = telescope(D_o, f_o, user_D_eye=D_eye)

    test_tel.add_eyepiece(test_eyepiece1,select=True)
    assert "0" in test_tel.eyepieces.keys()
    assert test_tel.current_eyepiece_id == "0"
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e1, fov_e1)
    
    test_tel.add_eyepiece(test_eyepiece2,select=True)
    assert "0" in test_tel.eyepieces.keys()
    assert "1" in test_tel.eyepieces.keys()
    assert test_tel.current_eyepiece_id == "1"
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e2, fov_e2)

    test_tel.add_eyepiece(test_eyepiece3,select=True)
    assert "0" in test_tel.eyepieces.keys()
    assert "1" in test_tel.eyepieces.keys()
    assert "2" in test_tel.eyepieces.keys()
    assert test_tel.current_eyepiece_id == "2"
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e3, fov_e3)

    test_tel.add_eyepiece(test_eyepiece3,id='Copy 3', select=True)
    assert "0" in test_tel.eyepieces.keys()
    assert "1" in test_tel.eyepieces.keys()
    assert "2" in test_tel.eyepieces.keys()
    assert "Copy 3" in test_tel.eyepieces.keys()
    assert test_tel.current_eyepiece_id == "Copy 3"
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e3, fov_e3)

    test_tel.select_eyepiece('1')
    assert "0" in test_tel.eyepieces.keys()
    assert "1" in test_tel.eyepieces.keys()
    assert "2" in test_tel.eyepieces.keys()
    assert "Copy 3" in test_tel.eyepieces.keys()
    assert test_tel.current_eyepiece_id == "1"
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e2, fov_e2)
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye)    

    test_tel.select_eyepiece()
    assert test_tel.current_eyepiece_id is None
    assert np.isnan(test_tel.M)
    assert np.isnan(test_tel.fov)
    assert np.isnan(test_tel.D_EP)
    assert np.isnan(test_tel.SB)

def test_focal_reducer_and_barlow_lens():
    """Check behavior of adding focal reducers/barlow lenses"""
    
    f_e = 10
    fov_e = 50
    test_eyepiece = eyepiece(f_e,fov_e)

    P_reducer = .5
    P_barlow = 2
    test_reducer = focal_reducer(P_reducer)
    test_barlow = barlow_lens(P_barlow)

    D_o = 100
    f_o = 100
    D_eye = 7
    test_tel = telescope(D_o, f_o, user_D_eye=D_eye)
    test_tel.add_eyepiece(test_eyepiece)
    test_tel.add_optic(test_reducer,id='reducer',select=False)
    test_tel.add_optic(test_barlow,id='Barlow lens',select=False)

    assert 'reducer' in test_tel.optics.keys()
    assert 'Barlow lens' in test_tel.optics.keys()
    assert test_tel.current_optic is None
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye)
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e, fov_e)

    test_tel.select_optic('reducer')
    assert test_tel.current_optic_id == 'reducer'
    assertions_for_tel_state(test_tel, f_o*P_reducer, D_o, D_eye)
    assertions_for_eyepieces(test_tel, f_o*P_reducer, D_o, f_e, fov_e)

    test_tel.select_optic('Barlow lens')
    assert test_tel.current_optic_id == 'Barlow lens'
    assertions_for_tel_state(test_tel, f_o*P_barlow, D_o, D_eye)
    assertions_for_eyepieces(test_tel, f_o*P_barlow, D_o, f_e, fov_e)

    test_tel.select_optic()
    assert test_tel.current_optic is None
    assertions_for_tel_state(test_tel, f_o, D_o, D_eye)
    assertions_for_eyepieces(test_tel, f_o, D_o, f_e, fov_e)

