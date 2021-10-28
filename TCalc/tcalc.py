"""Classes for handling telescope and eyepiece properties."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 14})
matplotlib.rcParams.update({'xtick.direction':'in'})
matplotlib.rcParams.update({'ytick.direction':'in'})
matplotlib.rcParams.update({'xtick.minor.visible':True})
matplotlib.rcParams.update({'ytick.minor.visible':True})
matplotlib.rcParams.update({'xtick.top':True})
matplotlib.rcParams.update({'ytick.right':True})
matplotlib.rcParams.update({'legend.frameon':False})
matplotlib.rcParams.update({'lines.dashed_pattern':[8,3]})
matplotlib.rcParams.update({"figure.figsize": [12,6]})

from TCalc.functions import focal_ratio, dawes_lim, resolving_power
from TCalc.functions import Min_magnification, Max_magnification, Min_eyepiece, Max_eyepiece
from TCalc.functions import Lmag_limit
from TCalc.functions import magnification, true_fov, exit_pupil, surface_brightness

from TCalc.age_eye import age_to_eye_diameter, eye_to_age

blue = 400
green = 550
red = 700
wavelengths_list = np.linspace(350,800,46)

age_list = np.array([10,20,30,35,45,60,70])
eye_diameter_list = np.array([age_to_eye_diameter(age) for age in age_list])

class eyepiece:
    """Class representing a single eyepiece
    Args:
        f_e: focal length of the eyepiece (mm) 
        fov_e: field of view of the eyepiece (deg). Defaults to 50 degrees.
    """
    def __init__(self, f_e, fov_e=50):

        if f_e <= 0:
            raise ValueError("f_e must be larger than 0")
        if fov_e <= 0:
            raise ValueError("fov must be larger than 0")

        self.f_e = f_e
        self.fov_e = fov_e

class focal_reducer:
    """Class representing a single focal reducer
    Args:
        P_reducer (float between 0 and 1): the power of the focal reducer
    """
    def __init__(self, P_reducer):

        if P_reducer <= 0 or P_reducer > 1:
            raise ValueError("P_reducer must be between 0 and 1")

        self.P = P_reducer
        self.optic_type = 'focal reducer'

class barlow_lens:
    """Class representing a single Barlow lens
    Args:
        barlow (float greater than 1): the Barlow factor, default is 2
    """
    def __init__(self, barlow=2):

        if barlow < 1:
            raise ValueError("barlow must be at least 1")

        self.P = barlow
        self.optic_type = 'Barlow lens'


class telescope:
    """Class representing a telescope
    Args:
        D_o: the size of the telescope opening (mm)
        f_o: focal length of the telescope (mm)
        user_D_eye: diameter of telescope user's eye in mm. Default is 7 mm.
        user_age: age of the telescope user. Will be used to compute user_D_eye if none is specified.
    """

    def __init__(self, D_o, f_o, user_D_eye=None, user_age=None):

        # Check that inputs make sense then save them as class atributes
        if D_o <= 0:
            raise ValueError("aperature must be larger than 0")
        if f_o <= 0:
            raise ValueError("f_o must be larger than 0")
        
        self.D_o = D_o
        self.f_o = f_o
        self.f_o_true = f_o

        # Some stuff about the user
        if user_D_eye is None:
            if user_age is None:
                print("No user_age or user_D_eye specified, using defaults (25 year old eye)")
                self.user_age = 25
                self.user_D_eye = age_to_eye_diameter(self.user_age)
            else:
                if user_age <= 0:
                    raise ValueError("user_age must be larger than 0")
                self.user_age = user_age
                self.user_D_eye = age_to_eye_diameter(self.user_age)
        else:
            if user_D_eye <= 0:
                raise ValueError("user_eye_aperature must be larger than 0")
            self.user_D_eye = user_D_eye
            if user_age is not None:
                print("Specified user_age and user_eye_aperature. The user_eye_aperature will be used for calculations.")
            self.user_age = user_age

        # Compute basic properties derived from telescope information alone
        self._compute_focal_ratio()
        self._compute_dawes_limit()
        self._compute_resolving_power()
        self._compute_min_mag()
        self._compute_max_mag()
        self._compute_min_eye()
        self._compute_max_eye()
        self._compute_magnitude_limit()

        # Initialize eyepiece information
        self.eyepieces = {}
        self.current_eyepiece_id = None
        self.current_eyepiece = None

        # Set properties that depend on eyepiece selection to NaNs
        self.M = np.nan
        self.compatible_eyepiece = False
        self.fov = np.nan
        self.D_EP = np.nan
        self.SB = np.nan

        # Initialize optic information
        self.optics = {}
        self.current_optic_id = None
        self.current_optic = None

    def list_eyepiece(self):
        """List the eyepieces and other optics availabe to the telescope
        Args:
            None
        Returns:
            Prints out a list of eyepiece objects and the
                current eyepiece being used.
        """

        print("\n   Currently included eyepieces:")
        print("     Name           Focal Length   FOV")
        print("     -------------- -------------- --------------")
        names = self.eyepieces.keys()
        for name in names:
            print("     {: <14} {: <14} {: <14} ".format("\'"+name+"\'", str(self.eyepieces[name].f_e)+" mm", str(self.eyepieces[name].fov_e)+" degrees"))
        
        if self.current_eyepiece is None:
            print("\n   No eyepiece is selected\n")
        else:
            print("\n   The currently selected eyepiece is '{}'\n".format(self.current_eyepiece_id))

        print("\n   Additional optical parts available:")
        print("     Name           Type           Power")
        print("     -------------- -------------- --------------")
        names = self.optics.keys()
        for name in names:
            print("     {: <14} {: <14} {: <14}".format("\'"+name+"\'", self.optics[name].optic_type, self.optics[name].P))
        
        if self.current_optic is None:
            print("\n   No optical part is selected\n")
        else:
            print("\n   The currently selected optical part is '{}'\n".format(self.current_optic_id))


    def select_eyepiece(self,id=None):
        """Set the current eyepiece
        Args:
            id: The id of the eyepiece to include. Default is None, which selects no eyepiece
        Returns:
            None
        """

        # If the ID is None, we'll get rid of the eyepiece
        if id is None:
            self.current_eyepiece = None
            self.current_eyepiece_id = None

            # Reset eyepiece dependent quantities to NaN
            self.M = np.nan
            self.compatible_eyepiece = False
            self.fov = np.nan
            self.D_EP = np.nan
            self.SB = np.nan

            return

        # Check that id is a valid input
        if ~isinstance(id,str):
            try:
                id = str(id)
            except:
                raise ValueError("id must be castable to type 'str'")

        # Check that id is in the eyepieces available
        if id not in self.eyepieces.keys():
            raise ValueError("id does not correspond to an eyepiece. Try self.list_eyepiece.")

        # Update eyepiece selection
        self.current_eyepiece_id = id
        self.current_eyepiece = self.eyepieces[id]

        # Update quantities dependent on eyepiece
        self._compute_magnification()
        if self.f_e_min <= self.current_eyepiece.f_e <= self.f_e_max:
            self.compatible_eyepiece = True
        else:
            self.compatible_eyepiece = False
            print("Note: The magnification produced by this eyepiece is not compatible with the telescope.")

        self._compute_true_fov()
        self._compute_exit_pupil()
        self._compute_surface_brightness_sensitivity()

    def select_optic(self,id=None):
        """Set the current optical part
        Args:
            id: The id of the optical part to include. Default is None, which selects no optical part
        Returns:
            None
        """

        # If the ID is None, we'll get rid of the eyepiece
        if id is None:
            self.current_optic = None
            self.current_optic_id = None
            
            # Update f_o 
            self.f_o = self.f_o_true

        # Check that id is a valid input
        else:
            if ~isinstance(id,str):
                try:
                    id = str(id)
                except:
                    raise ValueError("id must be castable to type 'str'")

            # Check that id is in the optics available
            if id not in self.optics.keys():
                raise ValueError("id does not correspond to an optical part. Try self.list_eyepiece.")

            # Update optic selection
            self.current_optic_id = id
            self.current_optic = self.optics[id]

            # Update f_o
            self.f_o = self.f_o_true * self.current_optic.P
        
        # Update other quantities
        self._compute_focal_ratio()
        self._compute_min_eye()
        self._compute_max_eye()

        if self.current_eyepiece is not None:
            self._compute_magnification()
            self._compute_true_fov()
            self._compute_exit_pupil()
            self._compute_surface_brightness_sensitivity()

            if self.f_e_min <= self.current_eyepiece.f_e <= self.f_e_max:
                self.compatible_eyepiece = True
            else:
                self.compatible_eyepiece = False
                print("Note: The magnification produced by this eyepiece is not compatible with the telescope.")

    def add_eyepiece(self, piece, id=None, select=True):
        """Attach an eyepiece to the telescope class
        The telescope class can have multiple eyepieces associated
        with it, this method allows you to add a single eyepiece 
        object to the list.
        Args:
            piece (eyepiece class instance): the eyepiece object to add
            id (string): the name to give the eyepiece - it will be identified by this name
            when selecting and analyzing eyepiece configurations. If unspecified, it will be set to a number.
            select (bool): if True (default) the added eyepiece will be selected by calling the select_eyepiece method.
        Returns:
            None
        """

        # If no name is given for eyepiece, just give it the index number as a name
        if id is None:
            id = str(len(self.eyepieces))
        # Check that inputs are formatted correctly
        elif ~isinstance(id,str):
            try:
                id = str(id)
            except:
                raise ValueError("id must be castable to type 'str'")
        if not isinstance(piece,eyepiece):
            raise ValueError("piece must be an instance of eyepiece class")

        # Add eyepiece to list
        self.eyepieces[id] = piece

        # If select==True, we'll make the new eyepiece the current eyepiece
        if select:
            self.select_eyepiece(id)

    def add_optic(self, optic, id=None, select=True):
        """Attach an optical part to the telescope class
        The telescope class can have multiple optical parts (focal reducers and Barlow lenses) 
        associated with it, this method allows you to add a single part to the list.
        Args:
            optic (focal_reducer or barlow_lens class instance): the optical part object to add
            id (string): the name to give the part - it will be identified by this name
            when selecting and analyzing optical configurations. If unspecified, it will be set to a number.
            select (bool): if True (default) the added optical part will be selected by calling the select_eyepiece method.
        Returns:
            None
        """

        # If no name is given for optic, just give it the index number as a name
        if id is None:
            id = str(len(self.optics))
        # Check that inputs are formatted correctly
        elif ~isinstance(id,str):
            try:
                id = str(id)
            except:
                raise ValueError("id must be castable to type 'str'")
        if not isinstance(optic,barlow_lens):
            if not isinstance(optic,focal_reducer):
                raise ValueError("optic must be an instance of barlow_lens or focal_reducer class")

        # Add eyepiece to list
        self.optics[id] = optic

        # If select==True, we'll make the new eyepiece the current eyepiece
        if select:
            self.select_optic(id)

    def change_user_age(self,new_age):
        """Update the age of the user and the corresponding eye size
        Args:
            new_age (float > 0): the age of the user
        Returns:
            None
        """

        # Some stuff about the user
        if new_age <= 0:
            raise ValueError("user_age must be larger than 0")
        self.user_age = new_age
        self.user_D_eye = age_to_eye_diameter(self.user_age)

        # Update limits
        self._compute_min_mag()
        self._compute_max_eye()

        # Update quantities dependent on eyepiece
        if self.current_eyepiece is not None:
            if self.f_e_min <= self.current_eyepiece.f_e <= self.f_e_max:
                self.compatible_eyepiece = True
            else:
                self.compatible_eyepiece = False
                print("Note: The magnification of the current eyepiece is not compatible.")


    def say_configuration(self):
        """List properties of the telescope eyepiece pair
        Args: 
            None
        Returns:
            Writes out the properties of the telescope
        """

        print("\n   The telescope has the following layout:")
        print("      Aperture Diameter:",'\033[1m' + '{} mm'.format(self.D_o) + '\033[0m')
        print("      Focal length:",'\033[1m' + '{} mm'.format(self.f_o_true) + '\033[0m', ", corresponding to a focal ratio of" ,'\033[1m' + '{} mm'.format(self.f_R_true) + '\033[0m')
        if self.current_optic is not None:
            if self.current_optic.optic_type == 'Barlow lens':
                action = 'increases'
            else:
                action = 'decreases'
            print("   '{}', a {}, has been added to the optical path. This {} the focal length by {}".format(self.current_optic_id,self.current_optic.optic_type,action,self.current_optic.P))
            print("   This results in")
            print("      Focal Length: {} mm, corresponding to a Focal Ratio of {}".format(self.f_o,self.f_R))
        print("")
        print("   In good atmospheric conditions, the resolution of the telescope (Dawes Limit) is", '\033[1m'+"{:.2f} arcseconds".format(self.Dawes_lim)+'\033[0m')
        print("   By wavelength, the resolution is")
        print("      {} nm (blue): {:.2f} arcsec".format(blue,self.blue_P_R))
        print("      {} nm (green): {:.2f} arcsec".format(green,self.green_P_R))
        print("      {} nm (red): {:.2f} arcsec".format(red,self.red_P_R))
        print("")

        age = eye_to_age(self.user_D_eye)
        print("   The", '\033[3m'+"maximum"+'\033[0m', "possible Magnification Factor is {:.2f}".format(self.M_max))
        print("   This means the", '\033[3m'+"minimum"+'\033[0m', "compatible eyepiece focal length is {:.2f} mm".format(self.f_e_min))
        print("")
        print("   The minimum magnification factor and corresponding maximum eyepiece focal length depend on the diameter of the observer's eye.")
        print("   For a telescope user with an eye diameter of {} mm (apropriate for an age around {} years):".format(self.user_D_eye,age))
        print("      The", '\033[3m'+"minimum"+'\033[0m', "Magnification Factor is {:.2f}".format(self.M_min))
        print("      This means the", '\033[3m'+"maximum"+'\033[0m', "compatible eyepiece focal length is {:.2f} mm".format(self.M_max))
        print("")
        print("   The", '\033[3m'+"faintest"+'\033[0m', "star that can be seen by this telescope is {:.3f} mag".format(self.Lmag_limit))

        if self.current_eyepiece is not None:
            print("")
            print("   The currently selected eyepiece is",'\033[1m' + '{}'.format(self.current_eyepiece_id) + '\033[0m',"which has the following layout:")
            print("      Focal Length:",'\033[1m' + '{} mm'.format(self.current_eyepiece.f_e) + '\033[0m')
            print("      Field of View:",'\033[1m' + '{} degrees'.format(self.current_eyepiece.fov_e)  + '\033[0m')
            print("")

            if self.compatible_eyepiece:
                compatible = 'is'
            else:
                compatible = 'IS NOT'
            print("   With this eyepiece:")
            print("      The Magnification Factor is",'\033[1m' + '{:.2f}'.format(self.M)  + '\033[0m', ". This {} compatible with the telescope limits.".format(compatible))
            print("      The True Field of View is",'\033[1m' + '{:.3f} degrees'.format(self.fov)  + '\033[0m')
            print("      The Exit Pupil Diameter is",'\033[1m' + "{:.2f} mm".format(self.D_EP)  + '\033[0m')
            print("")
            print("   The", '\033[3m'+"faintest"+'\033[0m', "surface brightness that can be seen by this telescope is", '\033[3m'+"{:.3f}".format(self.SB)+'\033[0m')
        print("")

    def show_resolving_power(self,seeing=2.5):
        """Plots the resolution performance of the telescope for a specific seeing value
        Args:
            seeing (float): Seeing factor of sky. Default to 2.5
        Returns:
            A plot depicting variation of chromatic resolution or simply the resolution at different wavelengths
            with respect to Dawes Limit and Limit due to seeing
        """
        fig,ax = plt.subplots()

        ax.set(xlabel='Wavelength [nm]', ylabel='Resolution [arcsec]',xlim=(380,750))
        ax.title.set_text('Resolution performance of the telescope-eyepiece pair')
        ax.plot(wavelengths_list,self.P_R,label='Chromatic Resolution')
        ax.axhline(self.Dawes_lim,color='C0',ls='--',label='Dawes limit')
        ax.axhline(seeing,color='.5',ls='--',label='Limit due to seeing')
        ax.legend()

        plt.show()

    def show_magnification_limits(self):
        """Plots the magnification limits for a telescope-eyepiece pair according to user's age
        Args:
            None
        Returns:
            Plot of maximum achievable magnification as a function of pupil's diameter
            which varies according to user's age. Also, plots the magnification strength's
            of the current selected eyepice.
        """
        fig,ax = plt.subplots()

        ax.set(xlabel='Eye Diameter [mm]', ylabel='Magnification Factor',xlim=(5,7.5),yscale='log')
        ax.title.set_text('Magnification Limits of the telescope-eyepiece pair')
        ax.plot(eye_diameter_list,self.M_min_by_age,ls='--',label='Minimum')
        ax.axhline(self.M_max,color='C0',label='Maximum')
        ax.axhline(self.M,color='k',label='Current Eyepiece')
        ax.legend()

        plt.show()

    def show_eyepiece_limits(self):
        """Plots the eyepiece limits for a telescope-eyepiece pair according to user's age and pupil diameter
        Args:
            None
        Returns:
            Plot of minimum achievable magnification as a function of pupil's diameter
            which varies according to user's age. Also, plots the power of the current selected eyepice.
        """
        fig,ax = plt.subplots()

        ax.set(xlabel='Eye Diameter [mm]', ylabel='Eyepiece Focal Length [mm]',xlim=(5,7.5))
        ax.title.set_text('Eyepiece Limits of the telescope-eyepiece pair')
        ax.plot(eye_diameter_list,self.f_e_max_by_age,ls='--',label='Maximum')
        ax.axhline(self.f_e_min,color='C0',label='Minimum')
        ax.axhline(self.current_eyepiece.f_e,color='k',label='Current Eyepiece')
        ax.legend()

        plt.show()


    # The rest of these are internal wrappers for running calculations in
    # functions.py. They get called by the automatically when something
    # about the telescope/eyepiece changes
    def _compute_focal_ratio(self):
        """Compute the focal ratio of the telescope
        Args:
            None
        Returns:
            Updates the state of self.f_R
        """

        self.f_R = focal_ratio(self.f_o,self.D_o)
        self.f_R_true = focal_ratio(self.f_o_true,self.D_o)

    def _compute_dawes_limit(self):
        """Compute the Dawes limit of the telescope-eyepiece pair
        Args:
            None
        Returns:
            Updates the state of self.Dawes_lim
        """

        self.Dawes_lim = dawes_lim(self.D_o)

    def _compute_resolving_power(self):
        """Compute the resolving power of the telescope vs wavelength
        Args:
            None
        Returns:
            Updates the state of self.resolving_power, and self.[color]_resolving_power
        """

        self.P_R = resolving_power(wavelengths_list,self.D_o)
        self.blue_P_R = resolving_power(blue,self.D_o)
        self.green_P_R = resolving_power(green,self.D_o)
        self.red_P_R = resolving_power(red,self.D_o)

    def _compute_min_mag(self):
        """Compute the minimum magnification of the telescope
        Args:
            None
        Returns:
            Updates the state of self.M_min and self.M_min_by_age
        """

        self.M_min = Min_magnification(self.D_o,self.user_D_eye)
        
        self.M_min_by_age = np.zeros(len(age_list))
        for i in range(len(age_list)):
            self.M_min_by_age[i] = Min_magnification(self.D_o,age=age_list[i])

    def _compute_max_mag(self):
        """Compute the maximum magnification of the telescope
        Args:
            None
        Returns:
            Updates the state of self.M_max
        """

        self.M_max = Max_magnification(self.D_o)

    def _compute_min_eye(self):
        """Compute the minimum eyepiece focal length compatible with the telescope
        Args:
            None
        Returns:
            Updates the state of self.f_e_min
        """

        self.f_e_min = Min_eyepiece(self.f_o,self.M_max)

    def _compute_max_eye(self):
        """Compute the maximum eyepiece focal length compatible with the telescope
        Args:
            None
        Returns:
            Updates the state of self.f_e_max and self.f_e_max_by_age
        """

        self.f_e_max = Max_eyepiece(self.f_R,self.user_D_eye)
        
        self.f_e_max_by_age = np.zeros(len(age_list))
        for i in range(len(age_list)):
            self.f_e_max_by_age[i] = Max_eyepiece(self.f_R,age=age_list[i])

    def _compute_magnitude_limit(self):
        """Compute the magnitude limit of the telescope
        Args:
            None
        Returns:
            Updates the state of self.Lmag_limit
        """

        self.Lmag_limit = Lmag_limit(self.D_o)

    def _compute_magnification(self):
        """Compute the magnification for the current telescope-eyepiece combo
        Args:
            None
        Returns:
            Updates the state of self.M
        """

        if self.current_eyepiece is None:
            raise ValueError("No eyepiece selected, cannot compute magnification")

        self.M = magnification(self.f_o,self.current_eyepiece.f_e)

    def _compute_true_fov(self):
        """Compute the true field of view of the telescope/eyepiece combo
        Args:
            None
        Returns:
            Updates the state of self.fov
        """

        if self.current_eyepiece is None:
            raise ValueError("No eyepiece selected, cannot compute magnification")

        self.fov = true_fov(self.M,self.current_eyepiece.fov_e)

    def _compute_exit_pupil(self):
        """Compute the exit pupil of the telescope/eyepiece combo
        Args:
            None
        Returns:
            Updates the state of self.D_EP
        """

        if self.current_eyepiece is None:
            raise ValueError("No eyepiece selected, cannot compute magnification")

        self.D_EP = exit_pupil(self.current_eyepiece.f_e,self.f_R)

    def _compute_surface_brightness_sensitivity(self):
        """Compute the surface brightness limit of the telescope/eyepiece combo
        Args:
            None
        Returns:
            Updates the state of self.SB
        """

        if self.current_eyepiece is None:
            raise ValueError("No eyepiece selected, cannot compute magnification")

        self.SB = surface_brightness(self.D_EP)
