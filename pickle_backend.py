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

"""Arch_Lab pickle serialization backend.

This module provides a serialization backend for the Arch_Lab program. You
probably should not be importing it directly.
"""

import pickle
import engine


class PickleFileBackend(engine.FileBackend):
    """FileBackend implementation for pickle format.

    Provides unified serialization interface to pickle for EngineConfig.
    """
    def save(target, item):
        with open(target, 'wb') as fil:
            pickle.dump(item, fil)

    def load(target):
        try:
            with open(target, 'rb') as fil:
                return pickle.load(fil)
        except (FileNotFoundError, EOFError):
            return ([], [])
