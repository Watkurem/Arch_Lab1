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

This module is a serialization backend for the Arch_Lab program. It exists to
provide unified serialization interface to pickle for engine. You probably
should not be importing it directly.
"""

import pickle


def save(target, item):
    """Serialize item into filename target. Create file or overwrite.

    target: string - file name.
    item: any python data structure - item to serialize.

    >>> import tempfile; import engine; \
    tmp = tempfile.NamedTemporaryFile(); \
    control = ([engine.Task("A", 1, 1, 1)], [engine.Task("B", 1000, 2, 3)]); \
    save(tmp.name, control); \
    tester = load(tmp.name); \
    control == tester
    True
    """
    with open(target, 'wb') as fil:
        pickle.dump(item, fil)


def load(target):
    """Deserialize filename target.

    Will return tuple of two empty lists if file does not exist.

    target: string - file name.
    return: any Python data structure or ([], [])

    >>> load("/im an idiot and store this file in root")
    ([], [])
    """
    try:
        with open(target, 'rb') as fil:
            return pickle.load(fil)
    except (FileNotFoundError, EOFError):
        return ([], [])
