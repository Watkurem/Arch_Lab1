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

def welcome(opts):
    print("Welcome to the Arch_Lab1 task planner!")
    return main_menu(opts)

def main_menu(opts):
    print("What would you like to do?\n")
    for option in opts:
        print("  [{}] {}".format(option[0], option[1]))
    return decide_main_menu(opts, input())

def decide_main_menu(opts, choice):
    choice = choice.upper()
    for option in opts:
        if choice == option[0]:
            return option
    print("Got {}! That's kinda wrong, try again.".format(choice))
    decide_main_menu(main_menu(opts))
    # if choice == opts[3][0]:
    #     exit()
    # elif choice == opts[0][0]:
    #     add_new_task()
    # elif choice == opts[1][0]:
    #     view_pending_tasks()
    # elif choice == opts[2][0]:
    #     view_finished_tasks()
    # else:
    #     print("Got {}! That's kinda wrong, try again.".format(choice))
    #     decide_main_menu(main_menu(opts))

def new_task_dialog():
    print("Creating new task.")
    content = input("Task description: ")
    date = input('Date (use "YYYY-MM-DD" format or similar ' +
                 'with single character delimiters): ')
    return (content, int(date[:4]), int(date[5:7]), int(date[8:10]))
