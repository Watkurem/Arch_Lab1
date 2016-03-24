# -*- coding: utf-8 -*-

###############################################################################
# Copyright 2016 Alexander Melnyk / Олександр Мельник
#
# This file is part of Arch_Lab1 package.
#
# Arch_Lab1 is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Arch_Lab1 is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Arch_Lab1. If not, see <http://www.gnu.org/licenses/>.
###############################################################################

import yaml

def save(target, item):
    """
    """
    with open(target, 'w') as fil:
        yaml.dump(item, fil)

def load(target):
    """
    """
    with open(target, 'r') as fil:
        test = yaml.load(fil)
        return test if test is not None else ([], [])
