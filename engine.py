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

"""Arch_Lab1 simple list engine.

This module is an engine ("model") for the Arch_Lab1 program. You probably
should not be importing it directly.

pending_task_list: list of pending tasks.
finished_task_list: list of finished tasks.
"""

import sys
import datetime
import bisect
import configparser


# class SaveFail(Exception):
#     pass

AVAILABLE_SAVEMETHODS =(('pickle', 'simple python-based object file format'),
                        ('json', 'JavaScript object notation'),
                        ('yaml', 'YAML file format'))
SAVEFILE = 'taskstorage'

config = configparser.ConfigParser()
config.read('config.ini')
try:
    config['DEFAULT']['savemethod']
except KeyError:
    config['DEFAULT']['savemethod'] = 'pickle'

# print(config['DEFAULT']['savemethod'])

# if config['DEFAULT']['savemethod'] == 'none':
#     file_backend = None
if config['DEFAULT']['savemethod'] == 'pickle':
    import pickle_backend as file_backend
    savefile = SAVEFILE + '.pkl'
elif config['DEFAULT']['savemethod'] == 'json':
    import json_backend as file_backend
    savefile = SAVEFILE + '.json'
elif config['DEFAULT']['savemethod'] == 'yaml':
    import yaml_backend as file_backend
    savefile = SAVEFILE + '.yaml'
else:
    print('WARNING: Config is broken!')
    sys.exit(1)


class Task:
    """Simple Task class.

    Sortable.

    content: string - task description.
    date: datetime.date - date task is scheduled on.
    """

    def __init__(self, content_, year, month, day):
        """Initialize Task instance.

        content: string - task description.
        year: int - year task is scheduled on.
        month: int - month task is scheduled on.
        day: int - day task is scheduled on.
        """
        self.content = content_
        self.date = datetime.date(year, month, day)

    def __lt__(self, other):
        """Task 'less than' comparison.

        Task is deemed less than another Task if it's date is less than
        another's.
        """
        return self.date < other.date

    def __hash__(self):
        """
        """
        return hash((self.content, self.date))

    def __eq__(self, other):
        """
        """
        try:
            return (self.content, self.date) == (other.content, other.date)
        except AttributeError:
            return NotImplemented

# For devtesting
# pending_task_list = [
#     Task("Задача тестова 3", 2016, 3, 1),
#     Task("Задача тестова 1", 2016, 3, 2),
#     Task("Задача тестова 2", 2016, 3, 3),
#     Task("Idle more cards", 2015, 10, 2),
#     Task("Sell cards for funbucks", 2015, 12, 2),
#     Task("Buy game for funbucks", 2015, 12, 10),
#     Task("Idle for even more cards", 2015, 12, 11),
#     Task("Consider selling soul to devil", 2015, 12, 11),
#     Task("Try to strike a deal with angels instead", 2015, 12, 20),
#     Task("Abandon all hope and play HL", 2015, 12, 31),
#     Task("Install Steam", 2012, 5, 29),
#     Task("Try playing some games", 2012, 6, 1),
#     Task("Leave message for sentient races of next universe", 2999, 1, 1),
# ]
# finished_task_list = []

pending_task_list, finished_task_list = file_backend.load(savefile)

pending_task_list.sort()
finished_task_list.sort()


def view_pending_tasks():
    """Fetch pending tasks.

    Converts pending_task_list from list of Task instances to a list of tuples.

    return: [(string, datetime.date), -||-]

    >>> import engine; \
    engine.pending_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    view_pending_tasks()
    [('Test task', datetime.date(2012, 12, 21))]
    """
    return [(task.content, task.date)
            for task in pending_task_list]


def new_task(content, year, month, day):
    """Add new task to pending_task_list.

    content: string - task description.
    year: int - year task is scheduled on.
    month: int - month task is scheduled on.
    day: int - day task is scheduled on.

    >>> import engine; engine.pending_task_list = []; \
    new_task("Test task", 2012, 12, 21); \
    (engine.pending_task_list[0].content, engine.pending_task_list[0].date)
    ('Test task', datetime.date(2012, 12, 21))
    """
    global pending_task_list
    bisect.insort(pending_task_list, Task(content, year, month, day))


def remove_pending_task(id):
    """Remove task from pending_task_list.

    id: int - descriptor, namely id of task in a list.

    >>> import engine; \
    engine.pending_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    remove_pending_task(0); \
    engine.pending_task_list
    []
    """
    pending_task_list.pop(id)


def edit_pending_task(id, content, year, month, day):
    """Edit task from pending_task_list.

    Replaces fields. Can also be implemented as 'delete, then add'.

    id: int - descriptor, namely id of task in a list.
    content: string - task description.
    year: int - year task is scheduled on.
    month: int - month task is scheduled on.
    day: int - day task is scheduled on.

    >>> import engine; \
    engine.pending_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    edit_pending_task(0, "Test edit", 9999, 1, 1); \
    [engine.pending_task_list[0].content, engine.pending_task_list[0].date]
    ['Test edit', datetime.date(9999, 1, 1)]
    """
    if content != "":
        pending_task_list[id].content = content
    if year is not None and month is not None and day is not None:
        pending_task_list[id].date = datetime.date(year, month, day)


def finish_task(id):
    """Move task from pending_task_list to finished_task_list.

    id: int - descriptor, namely id of task in a list.

    >>> import engine; \
    engine.pending_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    engine.finished_task_list = []; \
    finish_task(0); \
    [engine.pending_task_list, engine.finished_task_list[0].content]
    [[], 'Test task']
    """
    global pending_task_list
    global finished_task_list

    bisect.insort(finished_task_list, pending_task_list.pop(id))


def view_finished_tasks():
    """Fetch finished tasks.

    Converts finished_task_list from list of Task instances to a list of
    tuples.

    return: [(string, datetime.date), -||-]

    >>> import engine; \
    engine.finished_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    view_finished_tasks()
    [('Test task', datetime.date(2012, 12, 21))]
    """
    return [(task.content, task.date)
            for task in finished_task_list]


def clear_finished_tasks():
    """Clear finished task list.

    Actually just replaces finished_task_list with an empty one.

    >>> import engine; \
    engine.finished_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    clear_finished_tasks(); \
    engine.finished_task_list
    []
    """
    global finished_task_list
    finished_task_list = []


def remove_finished_task(id):
    """Remove task from finished_task_list.

    id: int - descriptor, namely id of task in a list.

    >>> import engine; \
    engine.finished_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    remove_finished_task(0); \
    engine.finished_task_list
    []
    """
    finished_task_list.pop(id)


def edit_finished_task(id, content, year, month, day):
    """Edit task from finished_task_list.

    Replaces fields. Can also be implemented as 'delete, then add'.

    id: int - descriptor, namely id of task in a list.
    content: string - task description.
    year: int - year task is scheduled on.
    month: int - month task is scheduled on.
    day: int - day task is scheduled on.

    >>> import engine; \
    engine.finished_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    edit_finished_task(0, "Test edit", 9999, 1, 1); \
    [engine.finished_task_list[0].content, engine.finished_task_list[0].date]
    ['Test edit', datetime.date(9999, 1, 1)]
    """
    if content != "":
        finished_task_list[id].content = content
    if year is not None and month is not None and day is not None:
        finished_task_list[id].date = datetime.date(year, month, day)


def unfinish_task(id):
    """Move task from finished_task_list to pending_task_list.

    id: int - descriptor, namely id of task in a list.

    >>> import engine; \
    engine.finished_task_list = [engine.Task("Test task", 2012, 12, 21)]; \
    engine.pending_task_list = []; \
    unfinish_task(0); \
    [engine.finished_task_list, engine.pending_task_list[0].content]
    [[], 'Test task']
    """
    global pending_task_list
    global finished_task_list

    bisect.insort(pending_task_list, finished_task_list.pop(id))


def save_tasks():
    """
    """
    # try:
    file_backend.save(savefile, (pending_task_list, finished_task_list))
    # except AttributeError:
    #     raise SaveFail("No save method selected")


def get_savemethod():
    """
    """
    return config['DEFAULT']['savemethod']


def get_available_savemethods():
    """
    """
    return AVAILABLE_SAVEMETHODS


def set_savemethod(method):
    """
    """
    config['DEFAULT']['savemethod'] = method
    with open('config.ini', 'w') as fil:
        config.write(fil)


def changes_detected():
    """
    """
    return file_backend.load(savefile) != (pending_task_list,
                                           finished_task_list)
