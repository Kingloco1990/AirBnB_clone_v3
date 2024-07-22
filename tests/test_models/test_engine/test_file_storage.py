#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""
import unittest
import inspect
import pep8
import json
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """
       Tests to check the documentation and style of file_storage module,
       the FileStorage class and its methods.
    """
    def test_module_docstring(self):
        """Test if the file_storage module has docstring."""
        self.assertIsNotNone(file_storage.__doc__,
                             'FileStorage lacks docstring')

    def test_class_docstring(self):
        """Test if the FileStorage class has docstring."""
        self.assertIsNotNone(FileStorage.__doc__,
                             'FileStorage lacks docstring')

    def test_method_docstrings(self):
        """Test if all methods in FileStorage class have docstrings."""
        for name, method in inspect.getmembers(FileStorage,
                                               predicate=inspect.isfunction):

            self.assertIsNotNone(
                method.__doc__, '{} method lacks a docstring'.format(name))


class TestPep8Compliance(unittest.TestCase):
    """
       Tests to check if file_storage and test_file_storage
       conform to PEP 8.
    """
    def test_pep8_compliance_file_storage(self):
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         ("Found code style errors (and warnings). "
                          "Total erros: {}".format(result.total_errors)))

    def test_pep8_compliance_test_file_storage(self):
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         ("Found code style errors (and warnings). "
                          "Total erros: {}".format(result.total_errors)))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db',
                     "Skipping because database storage is used")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db',
                     "Skipping because database storage is used")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db',
                     "Skipping because database storage is used")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db',
                     "Skipping because database storage is used")
    def test_get(self):
        """
        Test to check if the get method correctly retrieves an object
        based on its ID.
        """
        # Initialize FileStorage instance
        storage = FileStorage()

        # Save current state of __objects
        save = FileStorage._FileStorage__objects.copy()

        for key, cls in classes.items():
            with self.subTest(key=key, cls=cls):
                # Create an instance of the class and get its ID
                instance = cls()
                obj_id = instance.id

                # Add the instance to the storage
                storage.new(instance)

                # Assert that the get method returns the correct instance
                # based on its ID
                self.assertEqual(storage.get(instance, obj_id), instance)

        # Restore the original state of __objects
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db',
                     "Skipping because database storage is used")
    def test_count(self):
        """
        Test to check if the count method returns the correct number of
        objects stored in FileStorage.
        """
        # Initialize a FileStorage instance
        storage = FileStorage()

        # Save the current state of __objects
        save = FileStorage._FileStorage__objects.copy()

        # Define a dictionary of state classes
        state_classes = {
            "State1": State,
            "State2": State,
            "State3": State,
            "State4": State
        }

        # Select a specific class to count
        obj_class = state_classes["State1"]

        # Add instances of each class to the storage
        for cls in state_classes.values():
            storage.new(cls)

        # Count the number of objects currently stored in FileStorage
        count_obj = len(FileStorage._FileStorage__objects)

        # Assert that the storage.count method returns the correct
        # count for the selected class
        self.assertEqual(storage.count(obj_class), count_obj)

        # Restore the original state of __objects
        FileStorage._FileStorage__objects = save
