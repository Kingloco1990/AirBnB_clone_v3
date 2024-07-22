#!/usr/bin/python3
"""
Unit tests for the DBStorage class and its methods.
These tests ensure that the DBStorage class works correctly and
adheres to the expected behaviors.
"""

import unittest
import inspect
import pycodestyle
import models
from models.engine import db_storage
from models.engine.db_storage import DBStorage
from models.city import City
from models.state import State


class TestDBStorageDocs(unittest.TestCase):
    """
       Tests to check the documentation and style of db_storage module,
       the FileStorage class and its methods.
    """
    def test_module_docstring(self):
        """Test if the db_storage module has docstring."""
        self.assertIsNotNone(db_storage.__doc__,
                             'DBStorage lacks docstring')

    def test_class_docstring(self):
        """Test if the DBStorage class has docstring."""
        self.assertIsNotNone(DBStorage.__doc__,
                             'DBStorage lacks docstring')

    def test_method_docstrings(self):
        """Test if all methods in DBStorage class have docstrings."""
        for name, method in inspect.getmembers(DBStorage,
                                               predicate=inspect.isfunction):
            self.assertIsNotNone(
                method.__doc__, f'{name} method lacks a docstring')


class TestPep8Compliance(unittest.TestCase):
    """
       Tests to check if db_storage and test_db_storage
       conform to PEP 8.
    """
    def test_pep8_compliance_db_storage(self):
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         ("Found code style errors (and warnings). "
                          "Total erros: {}".format(result.total_errors)))

    def test_pep8_compliance_test_db_storage(self):
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         ("Found code style errors (and warnings). "
                          "Total erros: {}".format(result.total_errors)))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_get(self):
        """Test that get retrieves an object by class and ID"""
        storage = DBStorage
        new_state = State(name="Florida")
        storage.new(new_state)
        storage.save()
        result = storage.get(State, new_state.id)
        self.assertEqual(result, new_state)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_count(self):
        """Test that count returns the correct number of objects"""
        storage = DBStorage
        initial_count = storage.count()
        new_state = State(name="Texas")
        storage.new(new_state)
        storage.save()
        self.assertEqual(storage.count(), initial_count + 1)
        self.assertEqual(storage.count(State), 1)
