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

"""Arch_Lab engine implementations.

This module provides implementations of Engine class for Arch_Lab program. You
probably should not be importing it directly.
"""

import sys
import datetime
import bisect
import configparser
import lab
from lab import SAVEFILE
from lab import CONFIG

AVAILABLE_SAVEMETHODS = (('pickle', 'simple python-based object file format'),
                         ('json', 'JavaScript object notation'),
                         ('yaml', 'YAML file format'))


class FileBackend():
    """Abstract class/interface for file backend implementations for
    EngineConfig class.
    """
    def __init__(self):
        if type(self) is FileBackend:
            raise TypeError("FileBackend should not be instantiated")

    def save(target, item):
        """Serialize item into filename target. Create file or overwrite.

        target: string - file name.
        item: any python data structure - item to serialize.
        """
        raise NotImplementedError()

    def load(target):
        """Deserialize filename target.

        Will return tuple of two empty lists if file does not exist.

        target: string - file name.
        return: any Python data structure or ([], [])
        """
        raise NotImplementedError()


class EngineConfig(lab.Engine):
    """This class is intended to provide an unified configuration reading
    __init__ for other engines.

    Attributes:
      savefile - name of file in which tasks should be serialized. Is
                 controlled by SAVEFILE variable
      file_backend - FileBackend descendant that provides save/load
                     functionality.
    """
    def __init__(self):
        """Initialize self.

        Sets up file_backend as specified by config and savefile. Savefile
        extensions are hard-coded and savemethod-dependent, and file name is
        taken from SAVEFILE.

        Reads config parameter 'savemethod' and chooses file backend as
        follows to be stored as self.file_backend:
          pickle - pickle_backend.PickleFileBackend
          json - json_backend.JsonFileBackend
          yaml - yaml_backend.YamlFileBackend
        Will output an error message and finish the program if 'savemethod' is
        anything else.

        If 'savemethod' is not specified in config, pickle is chosen as
        default.
        """
        super().__init__()
        if type(self) is EngineConfig:
            raise TypeError("EngineConfig should not be instantiated")

        self.config = configparser.ConfigParser()
        self.config.read(CONFIG)
        try:
            self.config['DEFAULT']['savemethod']
        except KeyError:
            self.config['DEFAULT']['savemethod'] = 'pickle'

        if self.config['DEFAULT']['savemethod'] == 'pickle':
            from pickle_backend import PickleFileBackend as file_backend
            self.savefile = SAVEFILE + '.pkl'
        elif self.config['DEFAULT']['savemethod'] == 'json':
            from json_backend import JsonFileBackend as file_backend
            self.savefile = SAVEFILE + '.json'
        elif self.config['DEFAULT']['savemethod'] == 'yaml':
            from yaml_backend import YamlFileBackend as file_backend
            self.savefile = SAVEFILE + '.yaml'
        else:
            print('WARNING: Config is broken!')
            sys.exit(1)
        self.file_backend = file_backend

    def get_savemethod(self):
        return self.config['DEFAULT']['savemethod']

    def get_available_savemethods(self):
        """Get savemethods that are currently available.

        And their hopefully helpful descriptions. Available savemethods are
        specified by AVAILABLE_SAVEMETHODS variable.

        return: seq of two-item seqs ((string, string), -||-), where first item
                in every seq is a savemethod and second is it's hopefully
                helpful description.
        """
        return AVAILABLE_SAVEMETHODS

    def set_savemethod(self, method):
        """Change employed savemethod.

        Sets savefile and file_backend to new values and writes new savemethod
        into config.

        method: string - new savemethod to set.
        """
        self.config['DEFAULT']['savemethod'] = method
        with open(CONFIG, 'w') as fil:
            self.config.write(fil)

        if self.config['DEFAULT']['savemethod'] == 'pickle':
            from pickle_backend import PickleFileBackend as file_backend
            self.savefile = SAVEFILE + '.pkl'
        elif self.config['DEFAULT']['savemethod'] == 'json':
            from json_backend import JsonFileBackend as file_backend
            self.savefile = SAVEFILE + '.json'
        elif self.config['DEFAULT']['savemethod'] == 'yaml':
            from yaml_backend import YamlFileBackend as file_backend
            self.savefile = SAVEFILE + '.yaml'
        else:
            print('WARNING: Config is broken!')
            sys.exit(1)
        self.file_backend = file_backend


class ListEngine(EngineConfig):
    """Engine implementation for Arch_Lab.

    Extends EngineConfig with actual data management functionality.
    """
    def __init__(self):
        """Initialize self with tasks stored previously.

        Will call load function of self.file backend given by configuration for
        current pending and finished lists and accordingly generated filename.
        """
        super().__init__()
        (self.pending_task_list,
         self.finished_task_list) = self.file_backend.load(self.savefile)

    def view_pending_tasks(self):
        """Fetch pending tasks.

        Returns the list of stored pending tasks as a list of tuples.

        return: [(string, datetime.date), -||-]
        """
        return [(task.content, task.date)
                for task in self.pending_task_list]

    def new_task(self, content, year, month, day):
        bisect.insort(self.pending_task_list, Task(content, year, month, day))

    def remove_pending_task(self, id):
        """Remove task from the list of pending tasks.

        Will crash if task does not exist. Make sure you verify existence.

        id: int - descriptor, namely position of a task in the list.
        """
        self.pending_task_list.pop(id)

    def edit_pending_task(self, id, content, year, month, day):
        """Edit a task in the list of pending tasks.

        If content is "", description will not change. If either of year,
        month or date is None, all three of them will not change.

        id: int - descriptor, namely position of a task in the list.
        content: string - new task description.
        year: int - new year task is scheduled on.
        month: int - new month task is scheduled on.
        day: int - new day task is scheduled on.
        """
        if content != "":
            self.pending_task_list[id].content = content
        if year is not None and month is not None and day is not None:
            self.pending_task_list[id].date = datetime.date(year, month, day)

    def finish_task(self, id):
        bisect.insort(self.finished_task_list, self.pending_task_list.pop(id))

    def view_finished_tasks(self):
        """Fetch finished tasks.

        Returns the list of stored finished tasks as a list of tuples.

        return: [(string, datetime.date), -||-]
        """
        return [(task.content, task.date)
                for task in self.finished_task_list]

    def clear_finished_tasks(self):
        """Remove all finished tasks.

        List of finished tasks will be empty after this.
        """
        self.finished_task_list = []

    def remove_finished_task(self, id):
        """Remove task from the list of finished tasks.

        Will crash if task does not exist. Make sure you verify existence.

        id: int - descriptor, namely position of a task in the list.
        """
        self.finished_task_list.pop(id)

    def edit_finished_task(self, id, content, year, month, day):
        """Edit a task in the list of finished tasks.

        If content is "", description will not change. If either of year,
        month or date is None, all three of them will not change.

        id: int - descriptor, namely position of a task in the list.
        content: string - new task description.
        year: int - new year task is scheduled on.
        month: int - new month task is scheduled on.
        day: int - new day task is scheduled on.
        """
        if content != "":
            self.finished_task_list[id].content = content
        if year is not None and month is not None and day is not None:
            self.finished_task_list[id].date = datetime.date(year, month, day)

    def unfinish_task(self, id):
        bisect.insort(self.pending_task_list, self.finished_task_list.pop(id))

    def save_tasks(self):
        """Serialize task lists.

        Will serialize tasks using a FileBackend descendant. Refer to
        EngineConfig for details.
        """
        self.file_backend.save(self.savefile,
                               (self.pending_task_list,
                                self.finished_task_list))

    def changes_detected(self):
        return self.file_backend.load(
            self.savefile
        ) != (self.pending_task_list,
              self.finished_task_list)


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
        if not isinstance(content_, str):
            raise TypeError("Content must be string!")
        self.content = content_
        self.date = datetime.date(year, month, day)

    def __lt__(self, other):
        """Task 'less than' comparison.

        Task is deemed less than another Task if it's date is less than
        another's.
        """
        return self.date < other.date

    def __hash__(self):
        """Return hash(self).

        Task's hash will be same as (Task.content, Task.date).
        """
        return hash((self.content, self.date))

    def __eq__(self, other):
        """Return self == other.

        Tasks are deemed equal if both their fields are equal. As for now, Task
        instance can't be compared with anything except objects that quack like
        another Task instance, and attempt to compare with something else will
        raise a NotImplementedError exception.
        """
        try:
            return (self.content, self.date) == (other.content, other.date)
        except AttributeError:
            raise NotImplementedError

    def __repr__(self):
        return "{}('{}', {}, {}, {})".format("Task",
                                             self.content,
                                             self.date.year,
                                             self.date.month,
                                             self.date.day)
