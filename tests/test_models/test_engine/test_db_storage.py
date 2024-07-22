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
                          f"Total erros: {result.total_errors}"))

    def test_pep8_compliance_test_db_storage(self):
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         ("Found code style errors (and warnings). "
                          f"Total erros: {result.total_errors}"))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up for DBStorage tests"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Clean up after DBStorage tests"""
        self.storage.close()

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_all_no_class(self):
        """Test that all returns only specified class items"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()
        result = self.storage.all(State)
        self.assertIsInstance(result, dict)
        for key, value in result.items():
            self.assertIsInstance(value, State)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_new(self):
        """Test that new adds an object to the database session"""
        new_city = City(name="San Francisco", state_id="0001")
        self.storage.new(new_city)
        self.storage.save()
        result = self.storage.all(City)
        self.assertIn(f'City.{new_city.id}', result)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_save(self):
        """Test that save properly commits changes to the database"""
        new_city = City(name="Los Angeles", state_id="0002")
        self.storage.new(new_city)
        self.storage.save()
        result = self.storage.all(City)
        self.assertIn(f'City.{new_city.id}', result)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_delete(self):
        """Test that delete removes an object from the database session"""
        new_state = State(name="New York")
        self.storage.new(new_state)
        self.storage.save()
        self.storage.delete(new_state)
        self.storage.save()
        result = self.storage.all(State)
        self.assertNotIn(f'State.{new_state.id}', result)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_reload(self):
        """Test that reload correctly loads data from the database"""
        self.storage.reload()
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_get(self):
        """Test that get retrieves an object by class and ID"""
        new_state = State(name="Florida")
        self.storage.new(new_state)
        self.storage.save()
        result = self.storage.get(State, new_state.id)
        self.assertEqual(result, new_state)

    @unittest.skipIf(models.storage_t != 'db',
                     "Skipping because file storage is used")
    def test_count(self):
        """Test that count returns the correct number of objects"""
        initial_count = self.storage.count()
        new_state = State(name="Texas")
        self.storage.new(new_state)
        self.storage.save()
        self.assertEqual(self.storage.count(), initial_count + 1)
        self.assertEqual(self.storage.count(State), 1)
