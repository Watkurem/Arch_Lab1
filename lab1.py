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


tasks = list()

def main():
    OPTS = (
        ("N", "Add new task", add_new_task),
        ("L", "View pending tasks", view_pending_tasks),
        ("F", "View finished tasks", view_finished_tasks),
        ("Q", "Quit", quit)
    )
    interface.welcome(OPTS)[2]()

def add_new_task():
    engine.new_task(tasks, *interface.new_task_dialog())
    pass

def view_pending_tasks():
    pass

def view_finished_tasks():
    pass

if __name__=="__main__":
   main()
