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

import unittest
import unittest.mock as mock
import io
import copy
import random
import datetime
import string
import configparser
import pickle
import yaml
import json
import lab
import engine
import pickle_backend
import yaml_backend
import json_backend
from interface import TerminalInterface


class TestSuccess(Exception):
    pass


@mock.patch('pickle_backend.open')
class TestPickleBackend(unittest.TestCase):
    fbk = pickle_backend.PickleFileBackend
    testval = [123, 123]

    def setUp(self):
        self.fakefil = io.BytesIO()

    def test_save(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        self.fbk.save("/tmp/blah", self.testval)

        self.fakefil.seek(0)
        self.assertEqual(self.testval, pickle.load(self.fakefil))

    def test_read_correct(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        pickle.dump(self.testval, self.fakefil)

        self.fakefil.seek(0)
        self.assertEqual(self.testval, self.fbk.load(self.fakefil))

    def test_read_EOFError(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        pickle.dump(self.testval, self.fakefil)
        self.assertEqual(([], []), self.fbk.load("/tmp/blah"))

    def test_read_FileNotFoundError(self, mopen):
        mopen.side_effect = FileNotFoundError()
        self.assertEqual(([], []), self.fbk.load("/tmp/blah"))


@mock.patch('yaml_backend.open')
class TestYamlBackend(unittest.TestCase):
    fbk = yaml_backend.YamlFileBackend
    testval = [123, 123]

    def setUp(self):
        self.fakefil = io.StringIO()

    def test_save(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        self.fbk.save("/tmp/blah", self.testval)

        self.fakefil.seek(0)
        self.assertEqual(self.testval, yaml.load(self.fakefil))

    def test_read_correct(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        yaml.dump(self.testval, self.fakefil)

        self.fakefil.seek(0)
        self.assertEqual(self.testval, self.fbk.load(self.fakefil))

    def test_read_EOFError(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        yaml.dump(self.testval, self.fakefil)
        self.assertEqual(([], []), self.fbk.load("/tmp/blah"))

    def test_read_FileNotFoundError(self, mopen):
        mopen.side_effect = FileNotFoundError()
        self.assertEqual(([], []), self.fbk.load("/tmp/blah"))


@mock.patch('json_backend.open')
class TestJsonBackend(unittest.TestCase):
    fbk = json_backend.JsonFileBackend
    testval = [123, 123]
    Task_testval = ([engine.Task('123', 123, 1, 1)],
                    [engine.Task('1234', 132, 11, 11)])

    def setUp(self):
        self.fakefil = io.StringIO()

    def test_save_load_correct(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        self.fbk.save("/tmp/blah", self.Task_testval)

        self.fakefil.seek(0)
        self.assertEqual(self.Task_testval, self.fbk.load(self.fakefil))

    def test_save_not_Task(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        self.fbk.save("/tmp/blah", self.testval)

        self.fakefil.seek(0)
        self.assertEqual(self.testval, json.load(self.fakefil))

    def test_read_EOFError(self, mopen):
        mopen().__enter__.return_value = self.fakefil
        json.dump(self.testval, self.fakefil)
        self.assertEqual(([], []), self.fbk.load("/tmp/blah"))

    def test_read_FileNotFoundError(self, mopen):
        mopen.side_effect = FileNotFoundError()
        self.assertEqual(([], []), self.fbk.load("/tmp/blah"))


class TestTerminalInterface(unittest.TestCase):
    testopts = [["A", "abc"]]
    testtitle = "Blah"
    testdate = datetime.date.today()
    testtasks = [("abc", testdate - datetime.timedelta(days=1)),
                 ("XyZ", testdate),
                 ("", testdate + datetime.timedelta(days=1))]

    def test_init_TypeError(self):
        self.assertRaises(TypeError, TerminalInterface)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_welcome(self, mock_stdout):
        TerminalInterface.welcome()
        self.assertEqual(mock_stdout.getvalue(), "  \x1b[1mWelcome to the " +
                         "Arch_Lab task planner!\x1b[0m" + '\n')

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_menu(self, mock_stdout):
        TerminalInterface.menu(self.testopts, self.testtitle)
        correct_result = ("================================================================================\n"
                          "{}\n".format(self.testtitle))
        for x in self.testopts:
            correct_result += "  [{0[0]}] {0[1]}\n".format(x)
        self.assertEqual(mock_stdout.getvalue(), correct_result)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_decide_found(self, mock_stdout):
        c = random.randrange(0, len(self.testopts))
        ret = TerminalInterface.menu_decide(self.testopts, self.testopts[c][0])
        self.assertEqual(ret, self.testopts[c])

    def test_menu_decide_not_found(self):
        ret = TerminalInterface.menu_decide(self.testopts, "quack")
        self.assertEqual(ret, None)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_tasks_none_found(self, mock_stdout):
        correct_result = ("================================================================================\n"
                          "\t>> No tasks found <<\n")
        TerminalInterface.print_tasks([], False)
        self.assertEqual(mock_stdout.getvalue(), correct_result)
        mock_stdout.seek(0)
        TerminalInterface.print_tasks([], True)
        self.assertEqual(mock_stdout.getvalue(), correct_result)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_tasks_finished_true(self, mock_stdout):
        TerminalInterface.print_tasks(self.testtasks, True)
        correct_result = ("================================================================================\n" +
                          "[0]\t " + self.testtasks[0][1].strftime("%d %b %Y, %A:") + '\n' +
                          "  " + self.testtasks[0][0] + '\n\n'
                          "[1]\t " + self.testtasks[1][1].strftime("%d %b %Y, %A:") + '\n' +
                          "  " + self.testtasks[1][0] + '\n\n'
                          "[2]\t " + self.testtasks[2][1].strftime("%d %b %Y, %A:") + '\n' +
                          "  " + self.testtasks[2][0] + '\n')
        self.assertEqual(mock_stdout.getvalue(), correct_result)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_tasks_finished_false(self, mock_stdout):
        TerminalInterface.print_tasks(self.testtasks, False)
        correct_result = ("================================================================================\n" +
                          "[0]\t " + self.testtasks[0][1].strftime("%d %b %Y, %A:") + ' \x1b[1;31m<< !!OVERDUE!!\x1b[0m\n' +
                          "  " + self.testtasks[0][0] + '\n\n'
                          "[1]\t " + self.testtasks[1][1].strftime("%d %b %Y, %A:") + ' \x1b[1;32m<< Today!\x1b[0m\n' +
                          "  " + self.testtasks[1][0] + '\n\n'
                          "[2]\t " + self.testtasks[2][1].strftime("%d %b %Y, %A:") + '\n' +
                          "  " + self.testtasks[2][0] + '\n')
        self.assertEqual(mock_stdout.getvalue(), correct_result)

    @mock.patch('interface.TerminalInterface.print_tasks')
    def test_print_finished_tasks(self, mock_print_tasks):
        TerminalInterface.print_finished_tasks(self.testtasks)
        mock_print_tasks.assert_called_once_with(self.testtasks, True)

    @mock.patch('interface.input')
    @mock.patch('interface.TerminalInterface.menu')
    @mock.patch('interface.TerminalInterface.menu_decide')
    def test_finished_tasks_menu(self, mock_menu_decide,
                                 mock_menu, mock_input):
        foo = "foo"
        quack = "quack"
        mock_input.return_value = quack
        mock_menu_decide.return_value = foo
        self.assertEqual(foo,
                         TerminalInterface.finished_tasks_menu(self.testopts))
        mock_menu.assert_called_once_with(self.testopts,
                                          "You are viewing finished tasks")
        mock_menu_decide.assert_called_once_with(self.testopts, quack)

    @mock.patch('interface.TerminalInterface.print_tasks')
    def test_print_pending_tasks(self, mock_print_tasks):
        TerminalInterface.print_pending_tasks(self.testtasks)
        mock_print_tasks.assert_called_once_with(self.testtasks, False)

    @mock.patch('interface.input')
    @mock.patch('interface.TerminalInterface.menu')
    @mock.patch('interface.TerminalInterface.menu_decide')
    def test_pending_tasks_menu(self, mock_menu_decide,
                                mock_menu, mock_input):
        foo = "foo"
        quack = "quack"
        mock_input.return_value = quack
        mock_menu_decide.return_value = foo
        self.assertEqual(foo,
                         TerminalInterface.pending_tasks_menu(self.testopts))
        mock_menu.assert_called_once_with(self.testopts,
                                          "You are viewing pending tasks")
        mock_menu_decide.assert_called_once_with(self.testopts, quack)

    @mock.patch('interface.input')
    def test_ask_task_correct(self, mock_input):
        mock_input.return_value = "123"
        self.assertEqual(123, TerminalInterface.ask_task())

    @mock.patch('interface.input')
    def test_ask_task_wrong(self, mock_input):
        mock_input.return_value = "a"
        self.assertEqual(None, TerminalInterface.ask_task())

    @mock.patch('interface.input')
    def test_task_input_correct(self, mock_input):
        mock_input.side_effect = ["Descript", "1234-01-01"]
        self.assertEqual(("Descript", 1234, 1, 1),
                         TerminalInterface.task_input())

    @mock.patch('interface.input')
    def test_task_input_wrong(self, mock_input):
        mock_input.side_effect = ["", "1234-F7-01"]
        self.assertEqual(("", None, None, None),
                         TerminalInterface.task_input())

    @mock.patch('interface.TerminalInterface.task_input')
    def test_new_task_dialog(self, mock_task_input):
        mock_task_input.return_value = "quack"
        self.assertEqual("quack",
                         TerminalInterface.new_task_dialog())
        mock_task_input.assert_called_once_with()

    @mock.patch('interface.TerminalInterface.task_input')
    def test_edit_task_dialog(self, mock_task_input):
        mock_task_input.return_value = "quack"
        self.assertEqual("quack",
                         TerminalInterface.edit_task_dialog(random.randint))
        mock_task_input.assert_called_once_with()

    @mock.patch('interface.input')
    def test_bad_task(self, mock_input):
        mock_input.return_value = "a"
        self.assertEqual(None, TerminalInterface.bad_task())

    @mock.patch('interface.input')
    def test_bad_input(self, mock_input):
        mock_input.return_value = "a"
        self.assertEqual(None, TerminalInterface.bad_input())

    @mock.patch('interface.input')
    def test_save_dialog_no(self, mock_input):
        mock_input.return_value = "n"
        self.assertEqual(False, TerminalInterface.save_dialog())
        mock_input.return_value = "N"
        self.assertEqual(False, TerminalInterface.save_dialog())

    @mock.patch('interface.input')
    def test_save_dialog_others(self, mock_input):
        cases = string.printable.replace("n", "").replace("N", "")
        for c in cases:
            mock_input.return_value = c
            self.assertEqual(True, TerminalInterface.save_dialog())

    @mock.patch('interface.input')
    def test_config_menu_correct(self, mock_input):
        quack = "Quack"
        stls = (("asdf", "asfnoiewjndv"), ("123", "foobar"))
        cases = {x[0] for x in stls}
        for c in cases:
            mock_input.return_value = c
            self.assertEqual(c, TerminalInterface.config_menu(quack, stls))

    @mock.patch('interface.input')
    def test_config_menu_wrong(self, mock_input):
        quack = "Quack"
        stls = (("asdf", "asfnoiewjndv"), ("123", "foobar"))
        cases = ["Wrongchoice"]
        for c in cases:
            mock_input.return_value = c
            self.assertEqual(quack, TerminalInterface.config_menu(quack, stls))

    @mock.patch('interface.input')
    def test_config_menu_empty(self, mock_input):
        quack = "Quack"
        stls = (("asdf", "asfnoiewjndv"), ("123", "foobar"))
        cases = [""]
        for c in cases:
            mock_input.return_value = c
            self.assertEqual(quack, TerminalInterface.config_menu(quack, stls))


class TestFileBackend(unittest.TestCase):
    def test_init_TypeError(self):
        self.assertRaises(TypeError, engine.FileBackend)

    def test_save_NotImplementedError(self):
        self.assertRaises(NotImplementedError, engine.FileBackend.save, 1, 1)

    def test_load_NotImplementedError(self):
        self.assertRaises(NotImplementedError, engine.FileBackend.load, 1)


class TestEngineConfig(unittest.TestCase):
    def setUp(self):
        self.t = mock.MagicMock()

    def test_init_TypeError(self):
        self.assertRaises(TypeError, engine.EngineConfig)

    @mock.patch('engine.type', new=lambda x: False)
    @mock.patch('engine.sys.exit')
    @mock.patch('engine.configparser.ConfigParser')
    def test_init_config_broken(self, mock_ConfigParser, mock_exit):
        mock_exit.side_effect = TestSuccess
        with self.assertRaises(TestSuccess):
            engine.EngineConfig()
        mock_ConfigParser.assert_called_once_with()
        mock_exit.assert_called_once_with(1)

    @mock.patch('engine.type', new=lambda x: False)
    def test_init_config_pickle(self):
        mock_config = configparser.ConfigParser()
        mock_config.read = mock.MagicMock()
        mock_backend = mock.MagicMock()
        with mock.patch('engine.configparser.ConfigParser') as mock_CP:
            with mock.patch.dict('sys.modules', **{
                    'pickle_backend': mock_backend
            }):
                mock_CP.return_value = mock_config
                tmp = engine.EngineConfig()
                mock_CP.assert_called_once_with()
        self.assertEqual(tmp.config, mock_config)
        self.assertEqual(mock_config['DEFAULT']['savemethod'], 'pickle')
        self.assertEqual(tmp.file_backend, mock_backend.PickleFileBackend)
        self.assertEqual(tmp.savefile, lab.SAVEFILE + '.pkl')

    @mock.patch('engine.type', new=lambda x: False)
    def test_init_config_json(self):
        mock_config = configparser.ConfigParser()
        mock_config.read = mock.MagicMock()
        mock_config['DEFAULT']['savemethod'] = 'json'
        mock_backend = mock.MagicMock()
        with mock.patch('engine.configparser.ConfigParser') as mock_CP:
            with mock.patch.dict('sys.modules', **{
                    'json_backend': mock_backend
            }):
                mock_CP.return_value = mock_config
                tmp = engine.EngineConfig()
                mock_CP.assert_called_once_with()
        self.assertEqual(tmp.config, mock_config)
        self.assertEqual(mock_config['DEFAULT']['savemethod'], 'json')
        self.assertEqual(tmp.file_backend, mock_backend.JsonFileBackend)
        self.assertEqual(tmp.savefile, lab.SAVEFILE + '.json')

    @mock.patch('engine.type', new=lambda x: False)
    def test_init_config_yaml(self):
        mock_config = configparser.ConfigParser()
        mock_config.read = mock.MagicMock()
        mock_config['DEFAULT']['savemethod'] = 'yaml'
        mock_backend = mock.MagicMock()
        with mock.patch('engine.configparser.ConfigParser') as mock_CP:
            with mock.patch.dict('sys.modules', **{
                    'yaml_backend': mock_backend
            }):
                mock_CP.return_value = mock_config
                tmp = engine.EngineConfig()
                mock_CP.assert_called_once_with()
        self.assertEqual(tmp.config, mock_config)
        self.assertEqual(mock_config['DEFAULT']['savemethod'], 'yaml')
        self.assertEqual(tmp.file_backend, mock_backend.YamlFileBackend)
        self.assertEqual(tmp.savefile, lab.SAVEFILE + '.yaml')

    def test_get_savemethod(self):
        self.t.config = mock.MagicMock()
        self.t.testmeth = engine.EngineConfig.get_savemethod
        self.assertEqual(self.t.config['DEFAULT']['savemethod'],
                         self.t.testmeth(self.t))

    def test_get_available_savemethods(self):
        self.assertEqual(engine.AVAILABLE_SAVEMETHODS,
                         engine.EngineConfig.get_available_savemethods(self.t))

    @mock.patch('engine.sys.exit', side_effect=TestSuccess)
    @mock.patch('engine.open')
    def test_set_savemethod(self, mopen, mexit):
        self.t.config = configparser.ConfigParser()
        self.t.config.write = mock.MagicMock()
        self.t.testmeth = engine.EngineConfig.set_savemethod
        mock_backend = mock.MagicMock()

        self.assertRaises(TestSuccess, self.t.testmeth, self.t, 'puckle')
        mopen.assert_called_with(lab.CONFIG, 'w')
        self.assertTrue(self.t.config.write.called)
        self.assertEqual(self.t.config['DEFAULT']['savemethod'], 'puckle')

        with mock.patch.dict('sys.modules', **{
                'pickle_backend': mock_backend
        }):
            self.t.testmeth(self.t, 'pickle')
        mopen.assert_called_with(lab.CONFIG, 'w')
        self.assertTrue(self.t.config.write.called)
        self.assertEqual(self.t.config['DEFAULT']['savemethod'], 'pickle')
        self.assertEqual(self.t.file_backend, mock_backend.PickleFileBackend)
        self.assertEqual(self.t.savefile, lab.SAVEFILE + '.pkl')

        with mock.patch.dict('sys.modules', **{
                'json_backend': mock_backend
        }):
            self.t.testmeth(self.t, 'json')
        mopen.assert_called_with(lab.CONFIG, 'w')
        self.assertTrue(self.t.config.write.called)
        self.assertEqual(self.t.config['DEFAULT']['savemethod'], 'json')
        self.assertEqual(self.t.file_backend, mock_backend.JsonFileBackend)
        self.assertEqual(self.t.savefile, lab.SAVEFILE + '.json')

        with mock.patch.dict('sys.modules', **{
                'yaml_backend': mock_backend
        }):
            self.t.testmeth(self.t, 'yaml')
        mopen.assert_called_with(lab.CONFIG, 'w')
        self.assertTrue(self.t.config.write.called)
        self.assertEqual(self.t.config['DEFAULT']['savemethod'], 'yaml')
        self.assertEqual(self.t.file_backend, mock_backend.YamlFileBackend)
        self.assertEqual(self.t.savefile, lab.SAVEFILE + '.yaml')


class TestListEngine(unittest.TestCase):
    class Quack():
        def __init__(self, c, y, m, d):
            self.content = c
            self.date = datetime.date(y, m, d)

        def __lt__(self, other):
            return self.date < other.date

        def __eq__(self, other):
            return (self.content, self.date) == (other.content, other.date)

    testval = (['abc', 'efg'], ['asp', 'hgkrf'])
    testpen = [Quack("123", 1, 1, 1), Quack("abc", 2000, 10, 10)]
    testfin = [Quack("", 537, 7, 27), Quack("xyz", 9999, 12, 30)]

    def setUp(self):
        self.t = mock.MagicMock()
        self.t.pending_task_list = copy.deepcopy(self.testpen)
        self.t.finished_task_list = copy.deepcopy(self.testfin)

    def test_init(self):
        self.t.testmeth = engine.ListEngine.__init__
        self.t.file_backend.load = mock.MagicMock()
        self.t.file_backend.load.return_value = self.testval
        with mock.patch('engine.super'):
            self.t.testmeth(self.t)
        self.assertEqual((self.t.pending_task_list,
                          self.t.finished_task_list),
                         self.testval)
        self.t.file_backend.load.assert_called_once_with(self.t.savefile)

    def test_view_pending_tasks(self):
        self.t.testmeth = engine.ListEngine.view_pending_tasks
        correct = [("123", datetime.date(1, 1, 1)),
                   ("abc", datetime.date(2000, 10, 10))]
        self.assertEqual(correct, self.t.testmeth(self.t))

    @mock.patch('engine.Task', new=Quack)
    def test_new_task(self):
        self.t.testmeth = engine.ListEngine.new_task
        correct = [self.Quack("123", 1, 1, 1),
                   self.Quack("abc", 2000, 10, 10),
                   self.Quack("xyz", 9999, 12, 30)]
        self.t.testmeth(self.t, "xyz", 9999, 12, 30)
        self.assertEqual(correct, self.t.pending_task_list)

    def test_remove_pending_task(self):
        self.t.testmeth = engine.ListEngine.remove_pending_task
        id = random.randrange(0, len(self.testpen))
        correct = self.testpen[:id] + self.testpen[id+1:]
        self.t.testmeth(self.t, id)
        self.assertEqual(correct, self.t.pending_task_list)

    def test_edit_pending_task(self):
        self.t.testmeth = engine.ListEngine.edit_pending_task
        correct = [self.Quack("123", 1, 1, 1),
                   self.Quack("xyz", 9999, 12, 30)]
        self.t.testmeth(self.t, 1, "xyz", 9999, 12, 30)
        self.assertEqual(correct, self.t.pending_task_list)

    def test_finish_task(self):
        self.t.testmeth = engine.ListEngine.finish_task
        correct = ([self.Quack("123", 1, 1, 1)],
                   [self.Quack("", 537, 7, 27),
                    self.Quack("abc", 2000, 10, 10),
                    self.Quack("xyz", 9999, 12, 30)])
        self.t.testmeth(self.t, 1)
        self.assertEqual(correct, (self.t.pending_task_list,
                                   self.t.finished_task_list))

    def test_view_finished_tasks(self):
        self.t.testmeth = engine.ListEngine.view_finished_tasks
        correct = [("", datetime.date(537, 7, 27)),
                   ("xyz", datetime.date(9999, 12, 30))]
        self.assertEqual(correct, self.t.testmeth(self.t))

    def test_clear_finished_tasks(self):
        self.t.testmeth = engine.ListEngine.clear_finished_tasks
        correct = []
        self.t.testmeth(self.t)
        self.assertEqual(correct, self.t.finished_task_list)

    def test_remove_finished_task(self):
        self.t.testmeth = engine.ListEngine.remove_finished_task
        id = random.randrange(0, len(self.testpen))
        correct = self.testfin[:id] + self.testfin[id+1:]
        self.t.testmeth(self.t, id)
        self.assertEqual(correct, self.t.finished_task_list)

    def test_edit_finished_task(self):
        self.t.testmeth = engine.ListEngine.edit_finished_task
        correct = [self.Quack("123", 1, 1, 1),
                   self.Quack("xyz", 9999, 12, 30)]
        self.t.testmeth(self.t, 0, "123", 1, 1, 1)
        self.assertEqual(correct, self.t.finished_task_list)

    def test_unfinish_task(self):
        self.t.testmeth = engine.ListEngine.unfinish_task
        correct = ([self.Quack("123", 1, 1, 1),
                    self.Quack("", 537, 7, 27),
                    self.Quack("abc", 2000, 10, 10)],
                   [self.Quack("xyz", 9999, 12, 30)])
        self.t.testmeth(self.t, 0)
        self.assertEqual(correct, (self.t.pending_task_list,
                                   self.t.finished_task_list))

    def test_save_tasks(self):
        self.t.file_backend.save = mock.MagicMock()
        self.t.savefile = mock.MagicMock()
        self.t.testmeth = engine.ListEngine.save_tasks
        self.t.testmeth(self.t)
        self.t.file_backend.save.assert_called_with(
            self.t.savefile,
            (self.t.pending_task_list,
             self.t.finished_task_list))

    def test_changes_detected_T(self):
        self.t.file_backend.load = mock.MagicMock()
        self.t.file_backend.load.return_value = ([], [])
        self.t.testmeth = engine.ListEngine.changes_detected
        self.assertTrue(self.t.testmeth(self.t))
        self.t.file_backend.load.assert_called_with(self.t.savefile)

    def test_changes_detected_F(self):
        self.t.file_backend.load = mock.MagicMock()
        self.t.file_backend.load.return_value = (self.testpen, self.testfin)
        self.t.testmeth = engine.ListEngine.changes_detected
        self.assertFalse(self.t.testmeth(self.t))
        self.t.file_backend.load.assert_called_with(self.t.savefile)


class TestTask(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            engine.Task(1, 1, 1, 1)

    def test_lt(self):
        self.assertTrue(engine.Task("abc", 1, 1, 1) <
                        engine.Task("jewrovisa", 1, 1, 2))

    def test_hash(self):
        tmp = engine.Task("abc", 1, 1, 1)
        self.assertEqual(tmp.__hash__(),
                         hash(("abc", datetime.date(1, 1, 1))))

    def test_eq_other_quacks_like_task(self):
        x1 = engine.Task("abc", 1, 1, 1)
        x2 = engine.Task("abc", 1, 1, 1)
        self.assertEqual(x1, x2)
        self.assertIsNot(x1, x2)

    def test_eq_other_does_not_quack_like_task(self):
        x1 = engine.Task("abc", 1, 1, 1)
        x2 = ("abc", (1, 1, 1))
        with self.assertRaises(NotImplementedError):
            x1 == x2

    def test_repr(self):
        x1 = engine.Task("abc", 1, 1, 1)
        self.assertEqual("Task('abc', 1, 1, 1)", repr(x1))


class TestEngine(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, lab.Engine)

    def test_view_pending_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.view_pending_tasks,
                          None)

    def test_new_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.new_task,
                          None, None, None, None, None)

    def test_remove_pending_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.remove_pending_task,
                          None, None)

    def test_edit_pending_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.edit_pending_task,
                          None, None, None, None, None, None)

    def test_finish_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.finish_task,
                          None, None)

    def test_view_finished_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.view_finished_tasks,
                          None)

    def test_clear_finished_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.clear_finished_tasks,
                          None)

    def test_remove_finished_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.remove_finished_task,
                          None, None)

    def test_edit_finished_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.edit_finished_task,
                          None, None, None, None, None, None)

    def test_unfinish_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.unfinish_task,
                          None, None)

    def test_save_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.save_tasks,
                          None)

    def test_get_savemethod(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.get_savemethod,
                          None)

    def test_get_available_savemethods(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.get_available_savemethods,
                          None)

    def test_set_savemethod(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.set_savemethod,
                          None, None)

    def test_changes_detected(self):
        self.assertRaises(NotImplementedError,
                          lab.Engine.changes_detected,
                          None)


class TestController(unittest.TestCase):
    def test_init_TypeError(self):
        with self.assertRaises(TypeError):
            lab.Controller(None, None)

    @mock.patch('lab.type')
    def test_init_normal(self, mtype):
        i, e = "abc", "xyz"
        tmp = lab.Controller(i, e)
        self.assertEqual(i, tmp.interface)
        self.assertEqual(e, tmp.engine)

    def test_run(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.run,
                          None)

    def test_view_pending_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.view_pending_tasks,
                          None)

    def test_add_new_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.add_new_task,
                          None)

    def test_remove_pending_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.remove_pending_task,
                          None)

    def test_edit_pending_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.edit_pending_task,
                          None)

    def test_finish_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.finish_task,
                          None)

    def test_view_config_pending(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.view_config_pending,
                          None)

    def test_view_finished_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.view_finished_tasks,
                          None)

    def test_clear_finished_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.clear_finished_tasks,
                          None)

    def test_remove_finished_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.remove_finished_task,
                          None)

    def test_edit_finished_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.edit_finished_task,
                          None)

    def test_unfinish_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.unfinish_task,
                          None)

    def test_view_config_finished(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.view_config_finished,
                          None)

    def test_shutdown(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.shutdown,
                          None)

    def test_save_dialog(self):
        self.assertRaises(NotImplementedError,
                          lab.Controller.save_dialog,
                          None)


class TestInterface(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            lab.Interface()

    def test_welcome(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.welcome)

    def test_print_finished_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.print_finished_tasks,
                          None)

    def test_print_pending_tasks(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.print_pending_tasks,
                          None)

    def test_finished_tasks_menu(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.finished_tasks_menu,
                          None)

    def test_pending_tasks_menu(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.pending_tasks_menu,
                          None)

    def test_ask_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.ask_task)

    def test_new_task_dialog(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.new_task_dialog)

    def test_edit_task_dialog(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.edit_task_dialog,
                          None)

    def test_bad_task(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.bad_task)

    def test_bad_input(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.bad_input)

    def test_save_dialog(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.save_dialog)

    def test_config_menu(self):
        self.assertRaises(NotImplementedError,
                          lab.Interface.config_menu,
                          None, None)


class TestLabMain(unittest.TestCase):
    @mock.patch('lab.open')
    @mock.patch('lab.sys.exit', side_effect=TestSuccess)
    def test_main_argument(self, mexit, mopen):
        mock_config = configparser.ConfigParser()
        mock_config.read = mock.MagicMock()
        m_interface = mock.MagicMock()
        m_controller = mock.MagicMock()
        m_engine = mock.MagicMock()
        with mock.patch('engine.configparser.ConfigParser') as mock_CP:
            with mock.patch.dict('sys.modules', **{
                    'interface': m_interface,
                    'engine': m_engine,
                    'controller': m_controller,
            }):
                mock_CP.return_value = mock_config
                self.assertRaises(TestSuccess, lab.main)
        self.assertEqual(mock_config['DEFAULT']['controller'], 'argument')
        mock_config.read.assert_called_with(lab.CONFIG)
        m_controller.ArgumentController.assert_called_with(
            m_interface.TerminalInterface,
            m_engine.ListEngine()
        )
        m_controller.ArgumentController.return_value.run.assert_called_with()

    @mock.patch('lab.open')
    @mock.patch('lab.sys.exit', side_effect=TestSuccess)
    def test_main_simple(self, mexit, mopen):
        mock_config = configparser.ConfigParser()
        mock_config['DEFAULT']['controller'] = 'simple'
        mock_config.read = mock.MagicMock()
        m_interface = mock.MagicMock()
        m_controller = mock.MagicMock()
        m_engine = mock.MagicMock()
        with mock.patch('engine.configparser.ConfigParser') as mock_CP:
            with mock.patch.dict('sys.modules', **{
                    'interface': m_interface,
                    'engine': m_engine,
                    'controller': m_controller,
            }):
                mock_CP.return_value = mock_config
                self.assertRaises(TestSuccess, lab.main)
        self.assertEqual(mock_config['DEFAULT']['controller'], 'simple')
        mock_config.read.assert_called_with(lab.CONFIG)
        m_controller.SimpleController.assert_called_with(
            m_interface.TerminalInterface,
            m_engine.ListEngine()
        )
        m_controller.SimpleController.return_value.run.assert_called_with()


if __name__ == '__main__':
    unittest.main(buffer=True)
