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
    print("  \x1b[1mWelcome to the Arch_Lab1 task planner!\x1b[0m")

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
    print("Creating new task. It will be marked as pending.")
    return task_input()

def task_input():
    content = input("Task description: ")
    date = input('Date (use "YYYY-MM-DD" format or similar ' +
                 'with single character delimiters): ')
    try:
        return (content, int(date[:4]), int(date[5:7]), int(date[8:10]))
    except ValueError:
        return (content, None, None, None)

def print_finished_tasks(tasks):
    print_tasks(tasks, True)

def print_pending_tasks(tasks):
    print_tasks(tasks, False)

def print_tasks(tasks, finished):
    print("=" * 80)
    if tasks == []:
        print("\t>> No tasks found <<")
    else:
        for id, task in enumerate(tasks):
            print("[{}]\t".format(id), task[1].strftime("%d %b %Y, %A:"), end="")
            if not finished:
                if task[1] < task[1].today():
                    print(" \x1b[1;31m<< !!OVERDUE!!\x1b[0m", end="")
                elif task[1] == task[1].today():
                    print(" \x1b[1;32m<< Today!\x1b[0m", end="")
            print()
            print("  {}".format(task[0]))
            print()
        print("\x1b[A", end="")

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
    input("Task you asked for somehow does not exist. Press Return, check " +
          "the number and try again.")

def bad_input():
    input("You entered something we did not expect. Press Return and try again.")

def edit_task_dialog(id):
    print("Editing task {}.".format(id),
          "Enter new values or press Return to leave unchanged")
    return task_input()
