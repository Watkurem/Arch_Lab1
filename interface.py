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

"""Arch_Lab interface implementations.

This module provides implementations of Interface class for Arch_Lab program.
You probably should not be importing it directly.
"""

import locale
import lab

locale.setlocale(locale.LC_ALL, "en_US.utf8")


class TerminalInterface(lab.Interface):
    """Interface implementation for Arch_Lab.

    TerminalInterface provides a terminal interface to Arch_Lab task management
    functions.
    """
    def __init__(self):
        raise TypeError("TerminalInterface should not be instantiated")

    def welcome():
        """Print welcome message.

        Makes use of ANSI escape codes for formatting.
        """
        print("  \x1b[1mWelcome to the Arch_Lab task planner!\x1b[0m")

    def menu(opts, title):
        """Provide generic menu.

        Prints options determined by argument under title determined by
        argument.

        opts: list of lists which have at least two elements - (descriptor,
              option), both string - and each represent menu item.
              ((string, string, ...), -||-)
        title: title for the menu, string.
        """
        print("=" * 80, "\n", title, sep="")
        for option in opts:
            print("  [{}] {}".format(option[0], option[1]))

    def menu_decide(opts, choice):
        """Process user choice and return chosen option.

        Returns element of opts list that user have chosen. If user's choise
        does not correspond to any descriptor in opts, returns None, notifies
        user and asks to try again (calls menu_decide).
        Makes use of ANSI escape codes for formatting.

        opts: list of lists which have at least two elements - (descriptor,
              option), both string - and each represent menu item.
        choice: choice made by user (one of the descriptors in opts).

        return: chosen option (list that has at least two elements -
                (descriptor, option), both string) or None if there was no
                option corresponding to user's choice.
        """
        print("\x1b[A", " " * 80, "\x1b[A", sep="")
        choice = choice.upper()
        for option in opts:
            if choice == option[0]:
                return option
        return None

    def print_tasks(tasks, finished):
        """Print tasks.

        Prints tasks as formatted list. Date displayed according to locale.
        In 'pending' mode also marks tasks as 'overdue' or 'today'.

        tasks: ((string, datetime.date), -||-)
        finished: boolean. True  => 'finished' mode
                           False => 'pending' mode

        All branches tested in print_pending_tasks(), print_finished_tasks()
        """
        print("=" * 80)
        if tasks == []:
            print("\t>> No tasks found <<")
        else:
            for idx, task in enumerate(tasks):
                print("[{}]\t".format(idx), task[1].strftime("%d %b %Y, %A:"),
                      end="")
                if not finished:
                    if task[1] < task[1].today():
                        print(" \x1b[1;31m<< !!OVERDUE!!\x1b[0m", end="")
                    elif task[1] == task[1].today():
                        print(" \x1b[1;32m<< Today!\x1b[0m", end="")
                print()
                print("  {}".format(task[0]))
                if task is not tasks[-1]:
                    print()

    def print_finished_tasks(tasks):
        """Print finished tasks.

        Prints tasks as formatted list. Date displayed according to locale.

        tasks: ((string, datetime.date), -||-)
        """
        TerminalInterface.print_tasks(tasks, True)

    def finished_tasks_menu(opts):
        """Provide interactive finished tasks menu.

        Prints options determined by argument and allows user to choose one.

        opts: list of lists which have at least two elements - (descriptor,
              option), both string - and each represent menu item.
              ((string, string, ...), -||-)

        return: element of opts that was chosen by user.
        """
        TerminalInterface.menu(opts, "You are viewing finished tasks")
        return TerminalInterface.menu_decide(opts, input())

    def print_pending_tasks(tasks):
        """Print pending tasks.

        Prints tasks as formatted list. Date displayed according to locale.
        Tasks that are overdue (dated earlier than current date, but still
        pending) and tasks scheduled for current date will be marked
        accordingly.

        tasks: ((string, datetime.date), -||-)
        """
        TerminalInterface.print_tasks(tasks, False)

    def pending_tasks_menu(opts):
        """Provide interactive pending tasks menu.

        Prints options determined by argument and allows user to choose one.

        opts: list of lists which have at least two elements - (descriptor,
              option), both string - and each represent menu item.
              ((string, string, ...), -||-)

        return: element of opts that was chosen by user.
        """
        TerminalInterface.menu(opts, "You are viewing pending tasks")
        return TerminalInterface.menu_decide(opts, input())

    def ask_task():
        """Ask for a task descriptor.

        Should be used only after fresh (with no changes after printing yet)
        list of tasks was printed. Will ask to press Return and try again if
        input is not int.

        return: int - task descriptor, as input by user.
        """
        try:
            return int(input("Which one? Provide number noted in brackets: "))
        except ValueError:
            input("That was not a number. Press Return and try again.")
            return None

    def task_input():
        """Provide interactive dialog for task input.

        Used to add and edit tasks. Will ask user for task description (any
        string) and date in YYYY-MM-DD (with any single character delimiters).

        return: (str, int, int, int) if date read correctly,
                (str, None, None, None) if date not read correctly.
        """
        content = input("Task description: ")
        date = input('Date (use "YYYY-MM-DD" format or similar ' +
                     'with single character delimiters): ')
        try:
            return (content, int(date[:4]), int(date[5:7]), int(date[8:10]))
        except ValueError:
            return (content, None, None, None)

    def new_task_dialog():
        """Provide interactive dialog for adding new task.

        Prints status and calls task_input().

        return: (str, int, int, int) if date read correctly,
                (str, None, None, None) if date not read correctly.
        """
        print("Creating new task. It will be marked as pending.")
        return TerminalInterface.task_input()

    def edit_task_dialog(idx):
        """Provide interactive dialog for editing a task.

        Prints status and calls task_input().

        return: (str, int, int, int) if date read correctly,
                (str, None, None, None) if date not read correctly.
        """
        print("Editing task {}.".format(idx),
              "Enter new values or press Return to leave unchanged")
        return TerminalInterface.task_input()

    def bad_task():
        """Inform user that task is not there interactively.

        Namely, if user gave ask_task() an incorrect descriptor. Will also ask
        to press Return and try again.
        """
        input("Task you asked for somehow does not exist. Press Return, " +
              "check the number and try again.")

    def bad_input():
        """Inform user that they crashed the engine with their input.

        Congratulations! Will also ask to press Return and try again.
        """
        input("You entered something we did not expect. " +
              "Press Return and try again.")

    def save_dialog():
        """Provide interactive dialog for saving tasks.

        return: boolean - user's choice
        """
        print('Your task list differs from the one on disk. Do you wish to',
              'save changes?')
        choice = input('"N" for "No", any key for "Yes": ')
        return choice.upper() != 'N'

    def config_menu(current, available):
        """Provide interactive serialization configuration menu.

        current: string - method currently used for serialization.
        available: seq of two-item seqs ((string, string), -||-), where first
                   item in every seq is a serialization method and second is
                   it's hopefully helpful description.

        return: string - new serialization method.
        """
        print("=" * 80)
        print('The program is currently configured to save in', current,
              'format. If you wish to change that, available values are:')
        for x in available:
            print(' ', x[0], '-', x[1] + '.')
        print()
        choice = input('Enter new value (press Return to keep current one): ')
        if choice in {x[0] for x in available}:
            return choice
        elif choice == '':
            return current
        else:
            input('Wrong input. Configuration will not be changed. ' +
                  'Press Return and try again.')
            return current
