# -*- coding: utf-8 -*-

###############################################################################
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
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Arch_Lab1. If not, see <http://www.gnu.org/licenses/>.
###############################################################################

import datetime
import bisect


class Task:
    def __init__(self, content_, year, month, day):
        self.content = content_
        self.date = datetime.date(year, month, day)

    def __lt__(self, other):
        return self.date < other.date

# For devtesting
pending_task_list = [
    Task("Задача тестова 3", 2016, 3, 1),
    Task("Задача тестова 1", 2016, 3, 2),
    Task("Задача тестова 2", 2016, 3, 3),
    Task("Idle more cards", 2015, 10, 2),
    Task("Sell cards for funbucks", 2015, 12, 2),
    Task("Buy game for funbucks", 2015, 12, 10),
    Task("Idle for even more cards", 2015, 12, 11),
    Task("Consider selling soul to devil", 2015, 12, 11),
    Task("Try to strike a deal with angels instead", 2015, 12, 20),
    Task("Abandon all hope and play HL", 2015, 12, 31),
    Task("Install Steam", 2012, 5, 29),
    Task("Try playing some games", 2012, 6, 1),
    Task("Leave message for sentient races of next universe", 2999, 1, 1),
]
pending_task_list.sort()

finished_task_list = []
finished_task_list.sort()


def new_task(content, year, month, day):
    global pending_task_list
    bisect.insort(pending_task_list, Task(content, year, month, day))


def view_pending_tasks():
    return [(task.content, task.date)
            for task in pending_task_list]


def view_finished_tasks():
    return [(task.content, task.date)
            for task in finished_task_list]


def finish_task(id):
    global pending_task_list
    global finished_task_list

    bisect.insort(finished_task_list, pending_task_list.pop(id))


def unfinish_task(id):
    global pending_task_list
    global finished_task_list

    bisect.insort(pending_task_list, finished_task_list.pop(id))


def remove_finished_task(id):
    remove_task(id, True)


def remove_pending_task(id):
    remove_task(id, False)


def remove_task(id, finished):
    if finished:
        finished_task_list.pop(id)
    else:
        pending_task_list.pop(id)


def edit_finished_task(id, content, year, month, day):
    edit_task(id, content, year, month, day, True)


def edit_pending_task(id, content, year, month, day):
    edit_task(id, content, year, month, day, False)


def edit_task(id, content, year, month, day, finished):
    if finished:
        if content != "":
            finished_task_list[id].content = content
        if year is not None and month is not None and day is not None:
            finished_task_list[id].date = datetime.date(year, month, day)
    else:
        if content != "":
            pending_task_list[id].content = content
        if year is not None and month is not None and day is not None:
            pending_task_list[id].date = datetime.date(year, month, day)


def clear_finished_tasks():
    global finished_task_list
    finished_task_list = []
