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

import json
import engine
import datetime

class TaskJSONEncoder(json.JSONEncoder):
    def default (self, obj):
        if isinstance(obj, engine.Task):
            return {"__engine.Task__": True, **obj.__dict__}
        if isinstance(obj, datetime.date):
            return (obj.year, obj.month, obj.day)

def save(target, item):
    """
    """
    with open(target, 'w') as fil:
        json.dump(item, fil, cls = TaskJSONEncoder)

def load(target):
    """
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
