"""
Loads modules and submodules from files.
"""

import importlib
import importlib.util
import os


def load_module_from_file(module_name: str, file_path: str):
    """
    Loads a module from a file
    module_name is a unique name for the module. And a internal reference to the module.
    the module is executed when loaded
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path not found: {file_path}")

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not load spec for module {module_name} from {file_path}")

    if spec.loader is None:
        raise ImportError(f"No loader found for module {module_name} from {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def load_submodule_from_file(module_name: str, submodule_name: str, file_path: str):
    """
    Loads a submodule from a file
    module_name is a unique name for the module. And a internal reference to the module.
    submodule_name is the name of the submodule that should be loaded from the module
    e.g. a function or a class inside the file
    """
    module = load_module_from_file(module_name, file_path)
    submodule = getattr(module, submodule_name)

    return submodule


def load_module_attr(module_name: str, attr_name: str):
    """
    Loads an attribute from a module
    This is more secure because this methods does not execute the module
    """
    submodule = importlib.import_module(module_name)
    attr = getattr(submodule, attr_name)
    return attr
