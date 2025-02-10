# core/objects.py
import logging

logger = logging.getLogger(__name__)

class Object:
    def __init__(self, name, **properties):
        """
        A generic object that can participate in a sequence.
        :param name: Unique identifier for the object.
        :param properties: Arbitrary key-value pairs representing object attributes.
        """
        logger.debug(f"Creating new Object with name: {name}")
        logger.debug(f"Properties provided: {properties}")

        if not isinstance(name, str):
            logger.error(f"Invalid name type: {type(name)}. Must be string.")
            raise TypeError("Object name must be a string.")

        self.name = name
        # Properties remain mutable internally but shouldn't be altered externally
        self._properties = properties
        logger.info(f"Created Object: {self.name} with properties: {self._properties}")

    def get(self, property_name, default=None):
        """
        Retrieve a property, returning the default value if it doesn't exist.
        :param property_name: Name of the property to retrieve
        :param default: Value to return if property doesn't exist
        """
        value = self._properties.get(property_name, default)
        if value is None:
            logger.debug(f"Property '{property_name}' not found in object '{self.name}'")
        else:
            logger.debug(f"Retrieved property '{property_name}={value}' from '{self.name}'")
        return value

    def has_property(self, property_name):
        """Check if a property exists."""
        exists = property_name in self._properties
        logger.debug(f"Checking if '{self.name}' has property '{property_name}': {exists}")
        return exists

    def to_dict(self):
        """Converts the object into a dictionary representation."""
        return {"name": self.name, "properties": self._properties}

    def __str__(self):
        """Human-readable string representation."""
        props = [f"{k}={v}" for k, v in self._properties.items()]
        return f"Object({self.name}, {', '.join(props)})"

    def __repr__(self):
        """Detailed string representation."""
        return f"Object(name='{self.name}', properties={self._properties})"

    def __eq__(self, other):
        """Enables comparison between objects based on name and properties."""
        if not isinstance(other, Object):
            return NotImplemented
        return self.name == other.name and self._properties == other._properties

    def __hash__(self):
        """Ensures objects can be used in sets and dictionaries."""
        return hash((self.name, frozenset(self._properties.items())))
