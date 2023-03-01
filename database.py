"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""
import datetime
import operator as op
import filters as filt

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    
    def __init__(self,neos,cas):
        """Class object containing neos and approaches in useful data structures."""
        self._neos = neos
        self._approaches = cas
        
        #structure for get by des
        self.neo_des_dic = {}
        for neo in self._neos:
            self.neo_des_dic[neo.designation]= neo
          
        #structure for get by name
        self.neo_nam_dic = {}
        for neo in self._neos:
            if neo.name != None or neo.name != '':
                self.neo_nam_dic[neo.name]= neo
        
        #add diameter and hazardous values from neo to approach for neo
        for approach in self._approaches:
            approach.neo = self.neo_des_dic[approach.designation]
            approach.name = approach.neo.name
            approach.diameter = approach.neo.diameter
            approach.hazardous = approach.neo.hazardous
        
        #Link together the NEOs and their close approaches.
        for neo in self._neos:
            neo.approaches = [ca for ca in self._approaches if ca.designation == neo.designation]
        
            
    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return  self.neo_des_dic.get(designation)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        if name in self.neo_nam_dic.keys():
            return  self.neo_nam_dic.get(name)
        else:
            return None


    def query(self, filters={}):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            filter_results = []
            
            #dates
            if 'date' in filters.keys():
                filter_results.append(filt.DateFilter(filters['date'][0],filters['date'][1])(approach))  
            if 'start_date' in filters.keys():
                filter_results.append(filt.DateFilter(filters['start_date'][0],filters['start_date'][1])(approach))
            if 'end_date' in filters.keys():
                filter_results.append(filt.DateFilter(filters['end_date'][0],filters['end_date'][1])(approach))
            
            #distance
            if 'distance_min' in filters.keys():
                filter_results.append(filt.DistanceFilter(filters['distance_min'][0],filters['distance_min'][1])(approach))
            if 'distance_max' in filters.keys():
                filter_results.append(filt.DistanceFilter(filters['distance_max'][0],filters['distance_max'][1])(approach))
            
            #velocity    
            if 'velocity_min' in filters.keys():
                filter_results.append(filt.VelocityFilter(filters['velocity_min'][0],filters['velocity_min'][1])(approach))
            if 'velocity_max' in filters.keys():
                filter_results.append(filt.VelocityFilter(filters['velocity_max'][0],filters['velocity_max'][1])(approach))
            
            #diameter
            if 'diameter_min' in filters.keys():
                filter_results.append(filt.DiameterFilter(filters['diameter_min'][0],filters['diameter_min'][1])(approach))
            if 'diameter_max' in filters.keys():
                filter_results.append(filt.DiameterFilter(filters['diameter_max'][0],filters['diameter_max'][1])(approach))
              
            #hazardous
            if 'hazardous' in filters.keys():
                filter_results.append(filt.HazardousFilter(filters['hazardous'][0],filters['hazardous'][1])(approach))
            
            if all(filter_results):
                yield approach 
        