#!/usr/bin/env python
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

"""Arch_Lab main module ("controller"). Run this as a script or import and
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














































class Controller():
    """Abstract class/interface for controller implementations for Arch_Lab.

    A controller should implement all of these to be usable.

    Attributes:
      interface - Interface descendant.
      engine - Engine descendand instance.
    """
    def __init__(self, _interface, _engine):
        """Initialize self.

        _interface: Interface descendant - interface to be used.
        _engine: Engine descendant - engine to be used.
        """
        if type(self) is Controller:
            raise TypeError("Controller should not be instantiated")
        self.interface = _interface
        self.engine = _engine

    def run(self):
        """Execution should normally start here."""
        raise NotImplementedError()

    def view_pending_tasks(self):
        """Provide interactive view of pending tasks."""
        raise NotImplementedError()

    def add_new_task(self):
        """Add new task interactively."""
        raise NotImplementedError()

    def remove_pending_task(self):
        """Provide interactive way to remove one pending task."""
        raise NotImplementedError()

    def edit_pending_task(self):
        """Provide interactive way to edit one pending task."""
        raise NotImplementedError()

    def finish_task(self):
        """Mark pending task as finished interactively."""
        raise NotImplementedError()

    def view_config_pending(self):
        """Provide interactive configuration.

        As accessed from the view of pending tasks."""
        raise NotImplementedError()

    def view_finished_tasks(self):
        """Provide interactive view of finished tasks."""
        raise NotImplementedError()

    def clear_finished_tasks(self):
        """Remove all finished tasks."""
        raise NotImplementedError()

    def remove_finished_task(self):
        """Provide interactive way to remove one finished task."""
        raise NotImplementedError()

    def edit_finished_task(self):
        """Provide interactive way to edit one finished task."""
        raise NotImplementedError()

    def unfinish_task(self):
        """Mark finished task as pending."""
        raise NotImplementedError()

    def view_config_finished(self):
        """Provide interactive configuration.

        As accessed from the view of finished tasks."""
        raise NotImplementedError()

    def shutdown(self):
        """Execution should normally end here."""
        raise NotImplementedError()

    def save_dialog(self):
        """Provide interactive way to save tasks on exit."""
        raise NotImplementedError()
    """


if __name__ == "__main__":
    main()
