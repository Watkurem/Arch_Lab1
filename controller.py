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

import lab
import sys
import argparse


class SimpleController(lab.Controller):
    """Controller implementation for Arch_Lab.

    SimpleController supports connecting given interface and engine without any
    extra features.
    """
    def run(self):
        """Execution should normally start here.

        Displays welcome message and switches to pending task view.
        """
        self.interface.welcome()
        self.view_pending_tasks()

    def view_pending_tasks(self):
        """Provide interactive view of pending tasks.

        Tasks will be sorted by date from earliest to latest; tasks that are
        overdue (dated earlier than current date, but still pending) and tasks
        scheduled for current date will be marked accordingly.
        """
        PENDING_TASK_OPTS = (
            ("A", "Add new task", self.add_new_task),
            ("R", "Remove task", self.remove_pending_task),
            ("E", "Edit task", self.edit_pending_task),
            ("M", "Mark task finished", self.finish_task),
            ("F", "View finished tasks", self.view_finished_tasks),
            ("C", "Edit configuration", self.view_config_pending),
            ("Q", "Quit", self.shutdown)
        )

        self.interface.print_pending_tasks(self.engine.view_pending_tasks())
        try:
            self.interface.pending_tasks_menu(PENDING_TASK_OPTS)[2]()
        except TypeError:
            self.interface.bad_input()
            self.view_pending_tasks()

    def add_new_task(self):
        """Add new task interactively.

        Task will be marked pending by default. After task is added returns to
        the pending task view.
        """
        try:
            self.engine.new_task(*self.interface.new_task_dialog())
        except (TypeError, ValueError):
            self.interface.bad_input()

        self.view_pending_tasks()

    def remove_pending_task(self):
        """Provide interactive way to remove one pending task.

        After task is removed returns to the pending task view.
        """
        try:
            self.engine.remove_pending_task(self.interface.ask_task())
        except TypeError:
            pass
        except IndexError:
            self.interface.bad_task()

        self.view_pending_tasks()

    def edit_pending_task(self):
        """Provide interactive way to edit one pending task.

        After edits are done returns to the pending task view.
        """
        choice = self.interface.ask_task()
        args = self.interface.edit_task_dialog(choice)

        try:
            self.engine.edit_pending_task(choice, *args)
        except TypeError:
            pass
        except IndexError:
            self.interface.bad_task()
        except ValueError:
            self.interface.bad_input()

        self.view_pending_tasks()

    def finish_task(self):
        """Mark pending task as finished interactively.

        Afterwards returns to the pending task view.
        """

        try:
            self.engine.finish_task(self.interface.ask_task())
        except TypeError:
            pass
        except IndexError:
            self.interface.bad_task()

        self.view_pending_tasks()

    def view_config_pending(self):
        """Provide interactive configuration.

        As accessed from the view of pending tasks.

        Afterwards returns to the pending task view.
        """
        self.view_config()
        self.view_pending_tasks()

    def view_finished_tasks(self):
        """Provide interactive view of finished tasks.

        Tasks will be sorted by date from earliest to latest.
        """
        FINISHED_TASK_OPTS = (
            ("W", "Wipe finished tasks", self.clear_finished_tasks),
            ("R", "Remove task", self.remove_finished_task),
            ("E", "Edit task", self.edit_finished_task),
            ("M", "Mark task pending", self.unfinish_task),
            ("L", "View pending tasks", self.view_pending_tasks),
            ("C", "Edit configuration", self.view_config_finished),
            ("Q", "Quit", self.shutdown)
        )

        self.interface.print_finished_tasks(self.engine.view_finished_tasks())
        try:
            self.interface.finished_tasks_menu(FINISHED_TASK_OPTS)[2]()
        except TypeError:
            self.interface.bad_input()
            self.view_finished_tasks()

    def clear_finished_tasks(self):
        """Remove all finished tasks.

        Afterwards returns to the finished task view.
        """
        self.engine.clear_finished_tasks()
        self.view_finished_tasks()

    def remove_finished_task(self):
        """Provide interactive way to remove one finished task.

        After task is removed returns to the finished task view.
        """

        try:
            self.engine.remove_finished_task(self.interface.ask_task())
        except TypeError:
            pass
        except IndexError:
            self.interface.bad_task()

        self.view_finished_tasks()

    def edit_finished_task(self):
        """Provide interactive way to edit one finished task.

        After edits are done returns to the finished task view.
        """
        choice = self.interface.ask_task()
        args = self.interface.edit_task_dialog(choice)

        try:
            self.engine.edit_finished_task(choice, *args)
        except TypeError:
            pass
        except IndexError:
            self.interface.bad_task()
        except ValueError:
            self.interface.bad_input()

        self.view_finished_tasks()

    def unfinish_task(self):
        """Mark finished task as pending.

        Afterwards returns to the finished task view.
        """
        try:
            self.engine.unfinish_task(self.interface.ask_task())
        except TypeError:
            pass
        except IndexError:
            self.interface.bad_task()

        self.view_finished_tasks()

    def view_config_finished(self):
        """Provide interactive configuration.

        As accessed from the view of finished tasks.

        Afterwards returns to the finished task view.
        """
        self.view_config()
        self.view_finished_tasks()

    def shutdown(self):
        """Execution should normally end here.

        Calls save_dialog so that user can choose if tasks should be saved or
        not.
        """
        self.save_dialog()

    def save_dialog(self):
        """Provide interactive way to save tasks on exit."""
        if self.engine.changes_detected() and self.interface.save_dialog():
            self.engine.save_tasks()

    def view_config(self):
        """Provide interactive configuration."""
        t1, t2 = (self.engine.get_savemethod(),
                  self.engine.get_available_savemethods())
        tmp = self.interface.config_menu(t1, t2)
        self.engine.set_savemethod(tmp)


class ArgumentController(SimpleController):
    """Controller implementation for Arch_Lab.

    Extends SimpleController with command line argument functionality.
    """
    def run(self):
        """Execution should normally start here.

        If there were no arguments, displays welcome message and switches to
        pending task view.
        Otherwise processes arguments.
        """
        if len(sys.argv) > 1:
            self.process_args()
        else:
            super().run()

    def process_args(self):
        """Process arguments.

        Provides support for the following arguments:
        -h, --help      show help message and exit
        -a, --add       switch to task add dialogue
        -r, --remove    switch to task removal dialogue
        -e, --edit      switch to task edit dialogue
        -m, --mfinish   switch to finish task dialogue
        -f, --finished  switch to finished view
        -c, --config    switch to config dialogue
        """
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-a", "--add", action='store_true')
        group.add_argument("-r", "--remove", action='store_true')
        group.add_argument("-e", "--edit", action='store_true')
        group.add_argument("-m", "--mfinish", action='store_true')
        group.add_argument("-f", "--finished", action='store_true')
        group.add_argument("-c", "--config", action='store_true')
        args = parser.parse_args()
        if args.add:
            self.add_new_task()
        elif args.remove:
            self.remove_pending_task()
        elif args.edit:
            self.edit_pending_task()
        elif args.mfinish:
            self.finish_task()
        elif args.finished:
            self.view_finished_tasks()
        elif args.config:
            self.view_config_pending()
