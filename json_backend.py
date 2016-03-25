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

"""Arch_Lab JSON serialization backend.

This module is a serialization backend for the Arch_Lab program. It exists to
provide unified serialization interface to json for engine. You probably
should not be importing it directly.
"""

import json
import engine
import datetime


class TaskJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, engine.Task):
            return {"__engine.Task__": True, **obj.__dict__}
        if isinstance(obj, datetime.date):
            return (obj.year, obj.month, obj.day)


def save(target, item):
    """Serialize item into filename target. Create file or overwrite.

    target: string - file name.
    item: any json serializeable python data structure or engine.Task instance
          or datetime.date instance or any Python data structure containing any
          combination of those - item to serialize.

    >>> import tempfile; import engine; \
    tmp = tempfile.NamedTemporaryFile(mode="r+"); \
    control = ([engine.Task("A", 1, 1, 1)], [engine.Task("B", 1000, 2, 3)]); \
    save(tmp.name, control); \
    tester = load(tmp.name); \
    control == tester
    True
    """
    with open(target, 'w') as fil:
        json.dump(item, fil, cls=TaskJSONEncoder)


def load(target):
    """Deserialize filename target.

    Will return tuple of two empty lists if file does not exist.

    target: string - file name.
    return: ([engine.Task, -||-], [engine.Task, -||-])

    Tested in save()
    """
    try:
        with open(target, 'r') as fil:
            tmp1, tmp2 = json.load(fil)
            tmp1 = [engine.Task(x['content'],
                                x['date'][0], x['date'][1], x['date'][2])
                    for x in tmp1 if '__engine.Task__' in x.keys()]
            tmp2 = [engine.Task(x['content'],
                                x['date'][0], x['date'][1], x['date'][2])
                    for x in tmp2 if '__engine.Task__' in x.keys()]
            return (tmp1, tmp2)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return ([], [])
