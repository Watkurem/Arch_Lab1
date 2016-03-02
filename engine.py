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

import datetime


class Task:
    def __init__(self, content_, year, month, day):
        self.content = content_
        self.date = datetime.date(year, month, day)
        self.finished = None

# For devtesting
task_list = [
    Task("Задача тестова 1", 2016, 3, 2),
    Task("Задача тестова 2", 2016, 3, 3),
    Task("Задача тестова 3", 2016, 3, 1),
]

def new_task(content, year, month, day):
    global task_list
    task_list += [Task(content, year, month, day)]

def view_pending_tasks():
    return [(task.content, task.date)
            for task in task_list if task.finished is None]

def view_finished_tasks():
    return [(task.content, task.date)
            for task in task_list if task.finished is not None]
