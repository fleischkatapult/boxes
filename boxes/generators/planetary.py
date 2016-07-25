#!/usr/bin/env python3
# Copyright (C) 2013-2016 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
import math

class Planetary(Boxes):
    """Gearbox with multiple identical stages"""
    def __init__(self):
        Boxes.__init__(self)
        self.argparser.add_argument(
            "--sunteeth",  action="store", type=int, default=8,
            help="number of teeth on sun gear")
        self.argparser.add_argument(
            "--planetteeth",  action="store", type=int, default=20,
            help="number of teeth on planets")
        self.argparser.add_argument(
            "--modulus",  action="store", type=float, default=3,
            help="modulus of the theeth in mm")
        self.argparser.add_argument(
            "--shaft",  action="store", type=float, default=6.,
            help="diameter of the shaft")
        #self.argparser.add_argument(
        #    "--stages",  action="store", type=int, default=4,
        #    help="number of stages in the gear reduction")

    def render(self):
        # Initialize canvas
        self.open()

        ringteeth = self.sunteeth+2*self.planetteeth
        spoke_width = 3*self.shaft
        
        pitch1, size1, xxx = self.gears.sizes(teeth=self.sunteeth,
                                          dimension=self.modulus)
        pitch2, size2, xxx = self.gears.sizes(teeth=self.planetteeth,
                                          dimension=self.modulus)
        pitch3, size3, xxx = self.gears.sizes(
            teeth=ringteeth, internal_ring=True, spoke_width=spoke_width,
            dimension=self.modulus)

        t = self.thickness
        planets = int(math.pi//math.asin((self.planetteeth+2)/(self.planetteeth+self.sunteeth)))

        # Make sure the teeth mash
        ta = self.sunteeth+ringteeth
        # There are sunteeth+ringteeth mashing positions for the planets
        if ta % planets:
            planetpositions = [round(i*ta/planets)*360/ta for i in range(planets)]
        else:
            planetpositions = planets

        # XXX make configurable?
        profile_shift = 20
        pressure_angle = 20
        self.parts.disc(size3, lambda:self.hole(0,0,self.shaft/2), move="up")
        self.gears(teeth=ringteeth, dimension=self.modulus,
                   angle=pressure_angle, internal_ring=True,
                   spoke_width=spoke_width, mount_hole=self.shaft,
                   profile_shift=profile_shift, move="up")
        self.gears.gearCarrier(pitch1+pitch2, spoke_width, planetpositions,
                               2*spoke_width, self.shaft/2, move="up")
        self.gears(teeth=self.sunteeth, dimension=self.modulus,
                   angle=pressure_angle,
                   mount_hole=self.shaft, profile_shift=profile_shift, move="up")
        for i in range(planets):
            self.gears(teeth=self.planetteeth, dimension=self.modulus,
                       angle=pressure_angle,
                       mount_hole=self.shaft, profile_shift=profile_shift, move="up")
        
        self.close()

def main():
    b = Box()
    b.parseArgs()
    b.render()

if __name__ == '__main__':
    main()
