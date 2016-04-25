#!/usr/bin/env python
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

"""Arch_Lab main module. Run this as a script or import and run main().

Module itself provides abstract classes/interfaces for the program's 'building
blocks' - controller, interface ('view' in MVC) and engine ('model' in MVC).
"""


import sys
import configparser

CONFIG = 'config.ini'


class Engine():
    """Abstract class/interface for engine implementations for Arch_Lab.

    An engine should implement all of these to be usable."""
    def __init__(self):
        if type(self) is Engine:
            raise TypeError("Engine should not be instantiated")

    def view_pending_tasks(self):
        """Fetch pending tasks.

        Should return the list of stored pending tasks as a list of tuples.

        return: [(string, datetime.date), -||-]
        """
        raise NotImplementedError()

    def new_task(self, content, year, month, day):
        """Add new task to the list of pending tasks.

        content: string - task description.
        year: int - year task is scheduled on.
        month: int - month task is scheduled on.
        day: int - day task is scheduled on.
        """
        raise NotImplementedError()

    def remove_pending_task(self, id):
        """Remove task from the list of pending tasks.

        May crash if task does not exist.

        id: int - descriptor, namely position of a task in the list.
        """
        raise NotImplementedError()

    def edit_pending_task(self, id, content, year, month, day):
        """Edit a task in the list of pending tasks.

        If content is "", description should not change. If all of year,
        month and date are None, all three of them should not change. Other
        behaviour is implementation dependent.

        id: int - descriptor, namely position of a task in the list.
        content: string - new task description.
        year: int - new year task is scheduled on.
        month: int - new month task is scheduled on.
        day: int - new day task is scheduled on.
        """
        raise NotImplementedError()

    def finish_task(self, id):
        """Move task from the pending list to the finished list.

        id: int - descriptor, namely position of a task in a list.
        """
        raise NotImplementedError()

    def view_finished_tasks(self):
        """Fetch finished tasks.

        Should return the list of stored finished tasks as a list of tuples.

        return: [(string, datetime.date), -||-]
        """
        raise NotImplementedError()

    def clear_finished_tasks(self):
        """Remove all finished tasks.

        List of finished tasks should be empty after this.
        """
        raise NotImplementedError()

    def remove_finished_task(self, id):
        """Remove task from the list of finished tasks.

        May crash if task does not exist.

        id: int - descriptor, namely position of a task in the list.
        """
        raise NotImplementedError()

    def edit_finished_task(self, id, content, year, month, day):
        """Edit a task in the list of finished tasks.

        If content is "", description should not change. If all of year,
        month and date are None, all three of them should not change. Other
        behaviour is implementation dependent.

        id: int - descriptor, namely position of a task in the list.
        content: string - new task description.
        year: int - new year task is scheduled on.
        month: int - new month task is scheduled on.
        day: int - new day task is scheduled on.
        """
        raise NotImplementedError()

    def unfinish_task(self, id):
        """Move task from the finished list to the pending list.

        id: int - descriptor, namely position of a task in a list.
        """
        raise NotImplementedError()

    def save_tasks(self):
        """Store task lists.

        Should employ some method of storing currently used tasks so that they
        can be loaded later even if program was removed from memory.
        """
        raise NotImplementedError()

    def get_savemethod(self):
        """Get currently employed savemethod.

        Savemethod - some specific way to store task lists used by save_tasks.

        return: string - savemethod.
        """
        raise NotImplementedError()

    def get_available_savemethods(self):
        """Get savemethods that are currently available.

        And their hopefully helpful descriptions.

        Savemethod - some specific way to store task lists used by save_tasks.

        return: seq of two-item seqs ((string, string), -||-), where first item
                in every seq is a savemethod and second is it's hopefully
                helpful description.
        """
        raise NotImplementedError()

    def set_savemethod(self, method):
        """Change employed savemethod.

        Savemethod - some specific way to store task lists used by save_tasks.

        method: string - new savemethod to set.
        """
        raise NotImplementedError()

    def changes_detected(self):
        """Answers if task set changed.

        Specifically, if currently used task set differs from stored ones.
        """
        raise NotImplementedError()


class Controller():
    """Abstract class/interface for controller implementations for Arch_Lab.

    A controller should implement all of these to be usable.

    Attributes:
      interface - Interface descendant.
      engine - Engine descendand instance.
    """
    def __init__(self, _interface, _engine):
        """Initialize self.

        _interface: Interface descendant - interface to be used.
        _engine: Engine descendant - engine to be used.
        """
        if type(self) is Controller:
            raise TypeError("Controller should not be instantiated")
        self.interface = _interface
        self.engine = _engine

    def run(self):
        """Execution should normally start here."""
        raise NotImplementedError()

    def view_pending_tasks(self):
        """Provide interactive view of pending tasks."""
        raise NotImplementedError()

    def add_new_task(self):
        """Add new task interactively."""
        raise NotImplementedError()

    def remove_pending_task(self):
        """Provide interactive way to remove one pending task."""
        raise NotImplementedError()

    def edit_pending_task(self):
        """Provide interactive way to edit one pending task."""
        raise NotImplementedError()

    def finish_task(self):
        """Mark pending task as finished interactively."""
        raise NotImplementedError()

    def view_config_pending(self):
        """Provide interactive configuration.

        As accessed from the view of pending tasks."""
        raise NotImplementedError()

    def view_finished_tasks(self):
        """Provide interactive view of finished tasks."""
        raise NotImplementedError()

    def clear_finished_tasks(self):
        """Remove all finished tasks."""
        raise NotImplementedError()

    def remove_finished_task(self):
        """Provide interactive way to remove one finished task."""
        raise NotImplementedError()

    def edit_finished_task(self):
        """Provide interactive way to edit one finished task."""
        raise NotImplementedError()

    def unfinish_task(self):
        """Mark finished task as pending."""
        raise NotImplementedError()

    def view_config_finished(self):
        """Provide interactive configuration.

        As accessed from the view of finished tasks."""
        raise NotImplementedError()

    def shutdown(self):
        """Execution should normally end here."""
        raise NotImplementedError()

    def save_dialog(self):
        """Provide interactive way to save tasks on exit."""
        raise NotImplementedError()


class Interface():
    """Abstract class/interface for interface implementations for Arch_Lab.

    An interface should implement all of these to be usable.
    """
    def __init__(self):
        if type(self) is Interface:
            raise TypeError("Interface should not be instantiated")

    def welcome():
        """Provide welcome message."""
        raise NotImplementedError()

    def print_finished_tasks(tasks):
        """Provide view of finished tasks.

        tasks: ((string, datetime.date), -||-)
        """
        raise NotImplementedError()

    def finished_tasks_menu(opts):
        """Provide interactive finished tasks menu.

        opts: list of lists which have at least two elements - (descriptor,
              option), both string - and each represent menu item.
              ((string, string, ...), -||-)

        return: element of opts that was chosen by user.
        """
        raise NotImplementedError()

    def print_pending_tasks(tasks):
        """Provide view of pending tasks.

        tasks: ((string, datetime.date), -||-)
        """
        raise NotImplementedError()

    def pending_tasks_menu(opts):
        """Provide interactive pending tasks menu.

        opts: list of lists which have at least two elements - (descriptor,
              option), both string - and each represent menu item.
              ((string, string, ...), -||-)

        return: element of opts that was chosen by user.
        """
        raise NotImplementedError()

    def ask_task():
        """Ask for a task descriptor.

        return: int - task descriptor, as input by user.
        """
        raise NotImplementedError()

    def new_task_dialog():
        """Provide interactive dialog for adding new task.

        return: (content, year, month, day)
                (str, int, int, int) if date read correctly. If any part of
                date was read incorrectly, that part (or all three parts) may
                be replaced with None.
        """
        raise NotImplementedError()

    def edit_task_dialog(id):
        """Provide interactive dialog for editing a task.

        return: (content, year, month, day)
                (str, int, int, int) if date read correctly. If any part of
                date was read incorrectly, that part (or all three parts) may
                be replaced with None.
        """
        raise NotImplementedError()

    def bad_task():
        """Inform user that task is not there interactively."""
        raise NotImplementedError()

    def bad_input():
        """Inform user that they menace to crash the program with their input.
        """
        raise NotImplementedError()

    def save_dialog():
        """Provide interactive dialog for saving tasks.

        return: boolean - user's choice"""
        raise NotImplementedError()

    def config_menu(current, available):
        """Provide interactive serialization configuration menu.

        current: string - method currently used for serialization.
        available: seq of two-item seqs ((string, string), -||-), where first
                   item in every seq is a serialization method and second is
                   it's hopefully helpful description.

        return: string - new serialization method.
        """
        raise NotImplementedError()


def main():
    """Entry point for program."""
    import interface
    import engine
    import controller

    config = configparser.ConfigParser()
    config.read(CONFIG)
    try:
        config['DEFAULT']['controller']
    except KeyError:
        config['DEFAULT']['controller'] = 'argument'
        with open(CONFIG, 'w') as fil:
            config.write(fil)

    if config['DEFAULT']['controller'] == 'simple':
        ctr = controller.SimpleController
    else:
        ctr = controller.ArgumentController
    ctr(interface.TerminalInterface, engine.ListEngine()).run()
    sys.exit()


if __name__ == "__main__":
    main()
