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

import locale

locale.setlocale(locale.LC_ALL, "uk_UA.utf8")

def welcome():
    print("Welcome to the Arch_Lab1 task planner!")

def main_menu(opts):
    menu(opts, "\tMain menu")
    return menu_decide(opts, input())

def menu(opts, title):
    print("=" * 80,
          "\n",
          title,
          sep="")
    for option in opts:
        print("  [{}] {}".format(option[0], option[1]))

def menu_decide(opts, choice):
    print("\x1b[A", " " * 80, "\x1b[A", sep="")
    choice = choice.upper()
    for option in opts:
        if choice == option[0]:
            return option
    print("Got {}! That's kinda wrong, try again.".format(choice))
    menu_decide(main_menu(opts))

def new_task_dialog():
    print("Creating new task.")
    content = input("Task description: ")
    date = input('Date (use "YYYY-MM-DD" format or similar ' +
                 'with single character delimiters): ')
    return (content, int(date[:4]), int(date[5:7]), int(date[8:10]))

def print_tasks(tasks):
    if tasks == []:
        print("\n  >> No tasks found <<")
    for id, task in enumerate(tasks):
        print()
        print("[{}]".format(id), task[1].strftime("%d %b %Y, %A:"))
        print("\t", task[0])

def finished_tasks_menu(opts):
    menu(opts, "You are viewing finished tasks")
    return menu_decide(opts, input())

def pending_tasks_menu(opts):
    menu(opts, "You are viewing pending tasks")
    return menu_decide(opts, input())

def ask_task():
    try:
        return int(input("Which one? Provide number noted in brackets: "))
    except ValueError:
        input("That was not a number. Press Return and try again.")
        return None

def bad_task():
    print("Task you asked for somehow does not exist. Press Return, check",
          "the number and try again.")
