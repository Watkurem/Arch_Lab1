#!/usr/bin/env python

# -*- coding: utf-8 -*-

################################################################################
# Copyright 2015 Alexander Melnyk / Олександр Мельник
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
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Arch_Lab1. If not, see <http://www.gnu.org/licenses/>.
################################################################################

import interface
import engine

# "Просмотр задач" должен включать возможность добавить, удалить, редактировать,
# отметить завершённой, отметить незавершённой, очистить... That's about it?

def main():
    interface.welcome()
    main_menu()

def add_new_task():
    engine.new_task(*interface.new_task_dialog())

def view_pending_tasks():
    PENDING_TASK_OPTS = (
        ("N", "Add new task", add_new_task),
        ("R", "Remove task", remove_task),
        ("E", "Edit task", edit_task),
        ("M", "Mark task finished", finish_task),
        ("F", "View finished tasks", view_finished_tasks),
        ("Q", "Quit to main menu", main_menu)
    )

    interface.print_tasks(engine.view_pending_tasks())
    interface.pending_tasks_menu(PENDING_TASK_OPTS)[2]()

def view_finished_tasks():
    FINISHED_TASK_OPTS = (
        ("C", "Clear finished tasks", clear_finished_tasks),
        ("R", "Remove task", remove_task),
        ("E", "Edit task", edit_task),
        ("M", "Mark task pending", unfinish_task),
        ("L", "View pending tasks", view_pending_tasks),
        ("Q", "Quit to main menu", main_menu)
    )

    interface.print_tasks(engine.view_finished_tasks())
    interface.finished_tasks_menu(FINISHED_TASK_OPTS)[2]()

def remove_task():
    interface.ask_task()

def edit_task():
    interface.ask_task()

def finish_task():
    try:
        engine.finish_task(interface.ask_task())
    except TypeError:
        pass
    except IndexError:
        interface.bad_task()
    view_pending_tasks()

def main_menu():
    MAIN_MENU_OPTS = (
        ("N", "Add new task", add_new_task),
        ("L", "View pending tasks", view_pending_tasks),
        ("F", "View finished tasks", view_finished_tasks),
        ("Q", "Quit", quit_debug) # REPLACE WITH ACTUAL QUIT LATER
    )

    interface.main_menu(MAIN_MENU_OPTS)[2]()

def clear_finished_tasks():
    pass

def unfinish_task():
    try:
        engine.unfinish_task(interface.ask_task())
    except TypeError:
        print("Huh?")
    except IndexError:
        interface.bad_task()
    view_finished_tasks()

def quit_debug():
    pass

if __name__=="__main__":
    main()
