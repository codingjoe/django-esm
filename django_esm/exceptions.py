__all__ = ["ModuleNotFound"]


class ModuleNotFound(LookupError):
    """Raise when a module is absent from the import map.

    Attributes:
        module_name: Name of the requested module.
    """

    def __init__(self, module_name):
        self.module_name = module_name
        super().__init__(
            f"The import map has no entry for module {module_name!r}. "
            "Check that your package.json exports it and run the esm command."
        )
