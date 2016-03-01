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
# import engine

# "Просмотр задач" должен включать возможность добавить, удалить, редактировать,
# отметить завершённой, отметить незавершённой, очистить... That's about it?

OPTS = (
    "[N] Add new task",
    "[L] View pending tasks",
    "[F] View finished tasks",
    "[Q] Quit",
)

def main():
    interface.welcome()
    decide_main_menu(interface.main_menu(OPTS))
    # engine.

def decide_main_menu(choice):
    if choice == "Q":
        exit()
    elif choice == "N":
        add_new_task()
    elif choice == "L":
        view_pending_tasks()
    elif choice == "F":
        view_finished_tasks()
    else:
        print("Got {}! That's kinda wrong, try again.".format(choice))
        decide_main_menu(interface.main_menu(OPTS))

def add_new_task():
    pass

def view_pending_tasks():
    pass

def view_finished_tasks():
    pass

if __name__=="__main__":
   main()
