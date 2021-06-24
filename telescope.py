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

from functions import focal_ratio, dawes_lim, resolving_power
from functions import Min_magnification, Max_magnification, Min_eyepiece, Max_eyepiece
from functions import Lmag_limit
from functions import magnification, true_fov, exit_pupil, surface_brightness

from age_eye import age_to_eye_diameter, eye_to_age

blue = 400
green = 550
red = 700
wavelengths_list = np.linspace(350,800,46)

age_list = np.array([10,20,30,35,45,60,70])
eye_diameter_list = np.array([age_to_eye_diameter(age) for age in age_list])

class eyepiece:
    """Class representing a single eyepiece

    Initialization Args:
        flenght: focal length of the eyepiece in mm
        fov: field of view of the eyepiece in degrees. Defaults to 50 degrees.
    """
    def __init__(self, flength, fov=50):

        if flength <= 0:
            raise ValueError("flength must be larger than 0")
        if fov <= 0:
            raise ValueError("fov must be larger than 0")

        self.flength = flength
        self.fov = fov

class telescope:
    """Class representing a telescope

    Initialization Args:
        aperture: the size of the telescope opening in mm
        flenght: focal length of the telescope in mm
        user_eye_aperture: diameter of telescope user's eye in mm. Default is 7 mm.
        user_age: age of the telescope user. Will be used to compute user_eye_aperture if none is specified.
    """
    # TO DO: add user eye diameter stuff

    def __init__(self, aperture, flength, user_eye_aperture=None, user_age=None):

        # Check that inputs make sense then save them as class atributes
        if aperture <= 0:
            raise ValueError("aperature must be larger than 0")
        if flength <= 0:
            raise ValueError("flength must be larger than 0")
        
        self.aperture = aperture
        self.flength = flength

        # Some stuff about the user
        if user_eye_aperture is None:
            if user_age is None:
                print("No user_age or user_eye_aperture specified, using defaults (25 year old eye)")
                self.user_age = 25
                self.user_eye_aperture = age_to_eye_diameter(self.user_age)
            else:
                if user_age <= 0:
                    raise ValueError("user_age must be larger than 0")
                self.user_age = user_age
                self.user_eye_aperture = age_to_eye_diameter(self.user_age)
        else:
            if user_eye_aperture <= 0:
                raise ValueError("user_eye_aperature must be larger than 0")
            self.user_eye_aperture = user_eye_aperture
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
        self.magnification = np.nan
        self.compatible_eyepiece = False
        self.fov = np.nan
        self.exit_pupil = np.nan
        self.surface_brightness_sensitivity = np.nan


    def list_eyepiece(self):
        """List the eyepieces availabe to the telescope

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
            print("     {: <14} {: <14} {: <14} ".format("\'"+name+"\'", str(self.eyepieces[name].flength)+" mm", str(self.eyepieces[name].fov)+" degrees"))
        
        if self.current_eyepiece is None:
            print("\n   No eyepiece is selected\n")
        else:
            print("\n   The currently selected eyepiece is '{}'\n".format(self.current_eyepiece_id))


    def select_eyepiece(self,id=None):
        """Set the current eyepiece

        Args:
            id: The id of the eyepiece to include. Default is
                None, which selects no eyepiece
        Returns:
            None
        """

        # If the ID is None, we'll get rid of the eyepiece
        if id is None:
            self.current_eyepiece = None
            self.current_eyepiece_id = None

            # Reset eyepiece dependent quantities to NaN
            self.magnification = np.nan
            self.compatible_eyepiece = False
            self.fov = np.nan
            self.exit_pupil = np.nan
            self.surface_brightness_sensitivity = np.nan

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
        if self.min_eyepiece <= self.current_eyepiece.flength <= self.max_eyepiece:
            self.compatible_eyepiece = True
        else:
            self.compatible_eyepiece = False
            print("Note: The magnification produced by this eyepiece is not compatible with the telescope.")

        self._compute_true_fov()
        self._compute_exit_pupil()
        self._compute_surface_brightness_sensitivity()

    def add_eyepiece(self, piece, id=None, select=True):
        """Attach an eyepiece to the telescope class

        The telescope class can have multiple eyepieces associated
        with it, this method allows you to add a single eyepiece 
        object to the list.

        Args:
            piece (eyepiece class instance): the eyepiece object to add
            id (string): the name to give the eyepiece - it will be identified by this name
                when selecting and analyzing eyepiece configurations. If unspecified, it will 
                be set to a number.
            select (bool): if True (default) the added eyepiece will be selected by 
                calling the select_eyepiece method.
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

    def say_configuration(self):
        """List properties of the telescope eyepiece pair

        Args: 
            None
        Returns:
            Writes out the properties of the telescope
        """

        print("\n   The telescope has the following layout:")
        print("      Aperture diameter: {} mm".format(self.aperture))
        print("      Focal length: {} mm, corresponding to a focal ratio of {}".format(self.flength,self.focal_ratio))
        print("")
        print("   In good atmospheric conditions, the resolution of the telescope (Dawes limit) is {:.1f} arcseconds".format(self.dawes_limit))
        print("   By wavelength, the resolution is")
        print("      {} nm (blue): {:.1f} arcsec".format(blue,self.blue_resolving_power))
        print("      {} nm (green): {:.1f} arcsec".format(green,self.green_resolving_power))
        print("      {} nm (red): {:.1f} arcsec".format(red,self.red_resolving_power))
        print("")

        age = eye_to_age(self.user_eye_aperture)
        print("   The maximum possible magnification factor is {:.1f}".format(self.max_magnification))
        print("   This means the minimum compatible eyepiece focal length is {:.1f} mm".format(self.min_eyepiece))
        print("")
        print("   The minimum magnification factor and corresponding maximum eyepiece focal length depend on the diameter of the observer's eye.")
        print("   For a telescope user with an eye diameter of {} mm (apropriate for an age around {} years):".format(self.user_eye_aperture,age))
        print("      The minimum magnification factor is {:.1f}".format(self.min_magnification))
        print("      This means the maximum compatible eyepiece focal length is {:.1f} mm".format(self.max_magnification))
        print("")
        print("   The faintest star that can be seen by this telescope is {:.1f} mag".format(self.magnitude_limit))

        if self.current_eyepiece is not None:
            print("")
            print("   The currently selected eyepiece is '{}', which has the following layout:".format(self.current_eyepiece_id))
            print("      Focal length: {} mm".format(self.current_eyepiece.flength))
            print("      Field of view: {} degrees".format(self.current_eyepiece.fov))
            print("")

            if self.compatible_eyepiece:
                compatible = 'is'
            else:
                compatible = 'IS NOT'
            print("   With this eyepiece:")
            print("      The magnification factor is {:.1f}. This {} compatible with the telescope limits.".format(self.magnification,compatible))
            print("      The true field of view is {:.0f} degrees".format(self.fov))
            print("      The exit pupil diameter is {:.1f} mm".format(self.exit_pupil))
            print("")
            print("   The faintest surface brightness that can be seen by this telescope is {:.2f}".format(self.surface_brightness_sensitivity))
        print("")

    def show_resolving_power(self,seeing=2.5):

        fig,ax = plt.subplots()

        ax.set(xlabel='Wavelength [nm]', ylabel='Resolution [arcsec]',xlim=(380,750))
        ax.plot(wavelengths_list,self.resolving_power,label='Chromatic Resolution')
        ax.axhline(self.dawes_limit,color='C0',ls='--',label='Dawes limit')
        ax.axhline(seeing,color='.5',ls='--',label='Limit due to seeing')
        ax.legend()

        plt.show()

    def show_magnification_limits(self):

        fig,ax = plt.subplots()

        ax.set(xlabel='Eye Diameter [mm]', ylabel='Magnification Factor',xlim=(5,7.5),yscale='log')
        ax.plot(eye_diameter_list,self.min_mag_by_age,ls='--',label='Minimum')
        ax.axhline(self.max_magnification,color='C0',label='Maximum')
        ax.axhline(self.magnification,color='k',label='Current Eyepiece')
        ax.legend()

        plt.show()

    def show_eyepiece_limits(self):

        fig,ax = plt.subplots()

        ax.set(xlabel='Eye Diameter [mm]', ylabel='Eyepiece Focal Length [mm]',xlim=(5,7.5))
        ax.plot(eye_diameter_list,self.max_eye_by_age,ls='--',label='Maximum')
        ax.axhline(self.min_eyepiece,color='C0',label='Minimum')
        ax.axhline(self.current_eyepiece.flength,color='k',label='Current Eyepiece')
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
            Updates the state of self.focal_ratio
        """

        self.focal_ratio = focal_ratio(self.flength,self.aperture)

    def _compute_dawes_limit(self):
        """Compute the Dawes limit of the telescope

        Args:
            None
        Returns:
            Updates the state of self.dawes_limit
        """

        self.dawes_limit = dawes_lim(self.aperture)

    def _compute_resolving_power(self):
        """Compute the resolving power of the telescope vs wavelength

        Args:
            None
        Returns:
            Updates the state of self.dawes_limit
        """

        self.resolving_power = resolving_power(wavelengths_list,self.aperture)
        self.blue_resolving_power = resolving_power(blue,self.aperture)
        self.green_resolving_power = resolving_power(green,self.aperture)
        self.red_resolving_power = resolving_power(red,self.aperture)


    def _compute_min_mag(self):
        """Compute the minimum magnification of the telescope

        Args:
            None
        Returns:
            Updates the state of self.min_magnification and self.min_mag_by_age
        """

        self.min_magnification = Min_magnification(self.aperture,self.user_eye_aperture)
        
        self.min_mag_by_age = np.zeros(len(age_list))
        for i in range(len(age_list)):
            self.min_mag_by_age[i] = Min_magnification(self.aperture,age=age_list[i])

    def _compute_max_mag(self):
        """Compute the maximum magnification of the telescope

        Args:
            None
        Returns:
            Updates the state of self.max_magnification
        """

        self.max_magnification = Max_magnification(self.aperture)

    def _compute_min_eye(self):
        """Compute the minimum eyepiece focal length compatible with the telescope

        Args:
            None
        Returns:
            Updates the state of self.min_eyepiece
        """

        self.min_eyepiece = Min_eyepiece(self.aperture,self.max_magnification)

    def _compute_max_eye(self):
        """Compute the maximum eyepiece focal length compatible with the telescope

        Args:
            None
        Returns:
            Updates the state of self.max_eyepiece and self.max_eye_by_age
        """

        self.max_eyepiece = Max_eyepiece(self.focal_ratio,self.user_eye_aperture)
        
        self.max_eye_by_age = np.zeros(len(age_list))
        for i in range(len(age_list)):
            self.max_eye_by_age[i] = Max_eyepiece(self.focal_ratio,age=age_list[i])

    def _compute_magnitude_limit(self):
        """Compute the magnitude limit of the telescope

        Args:
            None
        Returns:
            Updates the state of self.magnitude_limit
        """

        self.magnitude_limit = Lmag_limit(self.aperture)

    def _compute_magnification(self):
        """Compute the magnification for the current telescope-eyepiece combo

        Args:
            None
        Returns:
            Updates the state of self.magnification
        """

        if self.current_eyepiece is None:
            raise ValueError("No eyepiece selected, cannot compute magnification")

        self.magnification = magnification(self.flength,self.current_eyepiece.flength)

    def _compute_true_fov(self):
        """Compute the true field of view of the telescope/eyepiece combo

        Args:
            None
        Returns:
            Updates the state of self.fov
        """

        self.fov = focal_ratio(self.magnification,self.current_eyepiece.fov)

    def _compute_exit_pupil(self):
        """Compute the exit pupil of the telescope/eyepiece combo

        Args:
            None
        Returns:
            Updates the state of self.exit_pupil
        """

        self.exit_pupil = exit_pupil(self.current_eyepiece.flength,self.focal_ratio)

    def _compute_surface_brightness_sensitivity(self):
        """Compute the surface brightness limit of the telescope/eyepiece combo

        Args:
            None
        Returns:
            Updates the state of self.exit_pupil
        """

        self.surface_brightness_sensitivity = surface_brightness(self.exit_pupil)