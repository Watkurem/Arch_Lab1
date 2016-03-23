#!/usr/bin/env python
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

"""Arch_Lab1 main module ("controller"). Run this as a script or import and
run main().

All functions are interactive and probably should not be run directly (only via
main()). Exact behaviour of each function depends on interface ("view") and
engine ("model") that implement them, but an attempt was made to describe
generally expected behaviour.

'Pending' means that task is not yet done. Finished means that task is done.
"""

import interface
import engine
import sys


def main():
    """Entry point for program.

    Displays welcome message and switches to pending task view.
    Start Arch_Lab1 by calling this function.
    """
    interface.welcome()
    view_pending_tasks()


def view_pending_tasks():
    """Provides interactive view of pending tasks.

    Tasks will be sorted by date from earliest to latest; tasks that are
    overdue (dated earlier than current date, but still pending) and tasks
    scheduled for current date will be marked accordingly.
    """
    PENDING_TASK_OPTS = (
        ("N", "Add new task", add_new_task),
        ("R", "Remove task", remove_pending_task),
        ("E", "Edit task", edit_pending_task),
        ("M", "Mark task finished", finish_task),
        ("F", "View finished tasks", view_finished_tasks),
        ("Q", "Quit", shutdown)
    )

    interface.print_pending_tasks(engine.view_pending_tasks())
    try:
        interface.pending_tasks_menu(PENDING_TASK_OPTS)[2]()
    except TypeError:
        interface.bad_input()
        view_pending_tasks()


def add_new_task():
    """Add new task interactively.

    Task will be marked pending by default. After task is added returns to the
    pending task view.
    """
    try:
        engine.new_task(*interface.new_task_dialog())
    except (TypeError, ValueError):
        interface.bad_input()

    view_pending_tasks()


def remove_pending_task():
    """Provides interactive way to remove one pending task.

    After task is removed returns to the pending task view.
    """
    try:
        engine.remove_pending_task(interface.ask_task())
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()

    view_pending_tasks()


def edit_pending_task():
    """Provides interactive way to edit one pending task.

    After edits are done returns to the pending task view.
    """
    choice = interface.ask_task()
    args = interface.edit_task_dialog(choice)

    try:
        engine.edit_pending_task(choice, *args)
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()
    except ValueError:
        interface.bad_input()

    view_pending_tasks()


def finish_task():
    """Mark pending task as finished interactively.

    Afterwards returns to the pending task view.
    """

    try:
        engine.finish_task(interface.ask_task())
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()

    view_pending_tasks()


def view_finished_tasks():
    """Provides interactive view of finished tasks.

    Tasks will be sorted by date from earliest to latest.
    """
    FINISHED_TASK_OPTS = (
        ("C", "Clear finished tasks", clear_finished_tasks),
        ("R", "Remove task", remove_finished_task),
        ("E", "Edit task", edit_finished_task),
        ("M", "Mark task pending", unfinish_task),
        ("L", "View pending tasks", view_pending_tasks),
        ("Q", "Quit", shutdown)
    )

    interface.print_finished_tasks(engine.view_finished_tasks())
    try:
        interface.finished_tasks_menu(FINISHED_TASK_OPTS)[2]()
    except TypeError:
        interface.bad_input()
        view_finished_tasks()


def clear_finished_tasks():
    """Remove all finished tasks.

    Afterwards returns to the finished task view.
    """
    engine.clear_finished_tasks()
    view_finished_tasks()


def remove_finished_task():
    """Provides interactive way to remove one finished task.

    After task is removed returns to the finished task view.
    """

    try:
        engine.remove_finished_task(interface.ask_task())
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()

    view_finished_tasks()


def edit_finished_task():
    """Provides interactive way to edit one finished task.

    After edits are done returns to the finished task view.
    """
    choice = interface.ask_task()
    args = interface.edit_task_dialog(choice)

    try:
        engine.edit_finished_task(choice, *args)
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()
    except ValueError:
        interface.bad_input()

    view_finished_tasks()


def unfinish_task():
    """Mark finished task as pending.

    Afterwards returns to the finished task view.
    """
    try:
        engine.unfinish_task(interface.ask_task())
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()

    view_finished_tasks()


def shutdown():
    """
    """
    # try:
    save_dialog()
    # except engine.SaveFail:
    #     interface.no_save_method_error()
    #     view_config()
    # else:
    sys.exit()


def save_dialog():
    """
    """
    if interface.save_dialog():
        engine.save_tasks()


if __name__ == "__main__":
    main()
