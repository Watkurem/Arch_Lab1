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

"""Arch_Lab YAML serialization backend.

This module is a serialization backend for the Arch_Lab program. It exists to
provide unified serialization interface to pyyaml for engine. You probably
should not be importing it directly.
"""

import yaml


def save(target, item):
    """Serialize item into filename target. Create file or overwrite.

    target: string - file name.
    item: any python data structure - item to serialize.

    >>> import tempfile; import engine; \
    tmp = tempfile.NamedTemporaryFile(mode="r+"); \
    control = ([engine.Task("A", 1, 1, 1)], [engine.Task("B", 1000, 2, 3)]); \
    save(tmp.name, control); \
    tester = load(tmp.name); \
    control == tester
    True
    """
    with open(target, 'w') as fil:
        yaml.dump(item, fil)


def load(target):
    """Deserialize filename target.

    Will return tuple of two empty lists if file does not exist.

    target: string - file name.
    return: any Python data structure or ([], [])

    Tested in save()
    """
    try:
        with open(target, 'r') as fil:
            test = yaml.load(fil)
    except (FileNotFoundError, EOFError):
        test = None
    return test if test is not None else ([], [])
