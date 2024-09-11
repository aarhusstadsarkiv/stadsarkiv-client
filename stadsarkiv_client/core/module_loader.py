"""
Loads modules and submodules from files.
"""

import importlib
import importlib.util
import os


def load_module_from_file(module_name: str, file_path: str):
    """
    Loads a module from a file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Settings file not found: {file_path}")

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
    """
    module = load_module_from_file(module_name, file_path)
    submodule = getattr(module, submodule_name)

    return submodule
