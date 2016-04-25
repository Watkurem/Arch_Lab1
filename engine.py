# -*- coding: utf-8 -*-

###############################################################################
# Copyright 2016 Alexander Melnyk / Олександр Мельник
#
# This file is part of Arch_Lab package.
#
# Arch_Lab is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Arch_Lab is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Arch_Lab. If not, see <http://www.gnu.org/licenses/>.
###############################################################################

"""Arch_Lab simple list engine.

This module is an engine ("model") for the Arch_Lab program. You probably
should not be importing it directly.

pending_task_list: list of pending tasks.
finished_task_list: list of finished tasks.
"""

import sys
import datetime
import bisect
import configparser

AVAILABLE_SAVEMETHODS = (('pickle', 'simple python-based object file format'),
                         ('json', 'JavaScript object notation'),
                         ('yaml', 'YAML file format'))


    """








    """






























