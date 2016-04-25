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

This module provides a serialization backend for the Arch_Lab program. You
probably should not be importing it directly.
"""

import json
import engine
import datetime


class JsonFileBackend(engine.FileBackend):
    """FileBackend implementation for JSON format.

    Provides unified serialization interface to json for EngineConfig.

    A very poor implementation seeing how JSON in Python is so problematic.
    Does not conform to interface in behaviour. Use at your own risk.
    """
    class TaskJSONEncoder(json.JSONEncoder):
        """Custom encoder to allow serialization of engine.Task and
        datetime.date
        """
        def default(self, obj):
            """Serialize engine.Task and datetime.date into JSON

            Pretty straight and dumb approach, Task into dict with
            "__engine.Task__": True pair and pairs for other fields, date into
            a tuple of it's three fields.
            """
            if isinstance(obj, engine.Task):
                return {"__engine.Task__": True, **obj.__dict__}
            elif isinstance(obj, datetime.date):
                return (obj.year, obj.month, obj.day)

    def save(target, item):
        """Serialize item into filename target. Create file or overwrite.

        target: string - file name.
        item: any json serializeable python data structure or engine.Task
              instance or datetime.date instance or any Python data structure
              containing any combination of those - item to serialize.
        """
        with open(target, 'w') as fil:
            json.dump(item, fil, cls=JsonFileBackend.TaskJSONEncoder)

    def load(target):
        """Deserialize filename target into two lists of Tasks.

        Will return tuple of two empty lists if file does not exist.

        target: string - file name.
        return: ([engine.Task, -||-], [engine.Task, -||-])
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
