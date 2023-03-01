"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str
from math import isnan
        
class NearEarthObject:
    """Create a new `NearEarthObject`."""
       
    def __init__(self, designation, name = None,
                 diameter = float('nan'), hazardous = False, **info):
        """Initialize NearEarth Object.
        
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        designation:  (string) NASA's unique identifer for the object
        name:  (string or None) IAU's name for the object, if named
        diameter: (float) The object's diameter in km
        hazardous: (Bool) NASA's designation for if object is potentially hazardous
        """
        if name == '':
            name = None
            
        if diameter == '':
            diameter = float('nan')
           
        if hazardous == 'Y':
            hazardous = True
        elif hazardous =='N':
            hazardous = False
        
        self.designation = str(designation)
        self.name = name
        self.diameter = float(diameter)
        self.hazardous = bool(hazardous)

        # Create an empty initial collection of linked approaches.
        self.approaches = []
    
    @property
    def fullname(self):
        """Represtination of the full name of this NEO."""
        if self.name == None:
            return f'{self.designation}'
        else: return f'{self.designation} {self.name}'

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous == True:
            hazard_desc = 'is'
        else: hazard_desc = 'is not'
            
        if isnan(self.diameter):
            return f'A Near Earth Object named {self.fullname} with '\
                f'an unknown diameter and {hazard_desc} potentially hazardus.'
        else:
            return f'A Near Earth Object named {self.fullname} has '\
                f'a diameter of {self.diameter} km and {hazard_desc} potentially hazardus.'

    def __repr__(self):
        """Computer-readable string representing this object."""
        return f"{self.designation!r}, {self.name!r}, " \
            f"{self.diameter:.3f}, {self.hazardous!r})"
            
            
class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    
    def __init__(self, designation, cd_time, distance=float('nan'), velocity=float('nan'), **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        designation: (string) unique identifier of the NEO
        time: UTC time in cad.json file format
        distance: nominal approach distance in au units
        velocity:  relative velocity to the approach body at close approach (v_rel from cad.json)
        """
        self.designation = designation
        self.time = cd_to_datetime(cd_time)  
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO for use within the database fil, initially set to None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.neo}' approached earth at a distance of {self.distance:.4f} au "\
            f"with a velocity of {self.velocity:.4f} km/s"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.4f}, " \
               f"velocity={self.velocity:.4f}, neo={self.neo!r})"
