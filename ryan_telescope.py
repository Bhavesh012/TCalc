import numpy as np
import matplotlib.pyplot as plt

from ryan_mag import compute_magnification

class eyepiece:
    """Class representing a single eyepiece

    Initialization Args:
        flenght: focal length of the eyepiece
        fov: field of view of the eyepiece
    """
    def __init__(self, flength, fov):

        if flength <= 0:
            raise ValueError("flength must be larger than 0")
        if fov <= 0:
            raise ValueError("fov must be larger than 0")

        self.flength = flength
        self.fov = fov
        
class telescope:
    """Class representing a telescope

    Initialization Args:
        aperture: the size of the telescope opening
        flenght: focal length of the telescope
    """

    def __init__(self, aperture, flength):

        if aperture <= 0:
            raise ValueError("aperature must be larger than 0")
        if flength <= 0:
            raise ValueError("flength must be larger than 0")
        
        self.aperture = aperture
        self.flength = flength
        self.eyepieces = {}

        self.current_eyepiece_id = None
        self.current_eyepiece = None

        self.magnification = np.nan

    def list_eyepiece(self):
        """List the eyepieces availabe to the telescope

        Args:
            None
        Returns:
            Prints out a list of eyepiece objects and the
                current eyepiece being used.
        """

        print("\n   Currently included eyepieces:")
        names = self.eyepieces.keys()
        for name in names:
            print("     '{}'".format(name))
        
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


        if id is None:
            self.current_eyepiece = None
            self.current_eyepiece_id = None

            self.magnification = np.nan

            return

        if ~isinstance(id,str):
            try:
                id = str(id)
            except:
                raise ValueError("id must be castable to type 'str'")

        if id not in self.eyepieces.keys():
            raise ValueError("id does not correspond to an eyepiece. Try self.list_eyepiece.")

        self.current_eyepiece_id = id
        self.current_eyepiece = self.eyepieces[id]

        self.compute_magnification()


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


        if id is None:
            id = str(len(self.eyepieces))
        elif ~isinstance(id,str):
            try:
                id = str(id)
            except:
                raise ValueError("id must be castable to type 'str'")
        if not isinstance(piece,eyepiece):
            raise ValueError("piece must be an instance of eyepiece class")

        self.eyepieces[id] = piece

        if select:
            self.select_eyepiece(id)

    def compute_magnification(self):
        """Compute the magnification for the current telescope-eyepiece combo

        Args:
            None
        Returns:
            Updates the state of self.magnification
        """


        if self.current_eyepiece is None:
            raise ValueError("No eyepiece selected, cannot compute magnification")

        self.magnification = compute_magnification(self.flength,self.current_eyepiece.flength)

