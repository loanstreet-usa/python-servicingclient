from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Callable, Iterable, Set, Union

from ...errors import ServicingObjectFormationError


class BaseObject:
    def __str__(self):
        return f"<servicing.{self.__class__.__name__}>"


class JsonObject(BaseObject, metaclass=ABCMeta):
    @property
    @abstractmethod
    def attributes(self) -> Set[str]:
        """Provide a set of attributes of this object that will make up its JSON structure"""
        return set()

    def validate_json(self) -> None:
        """
        Raises:
          ServicingObjectFormationError if the object was not valid
        """
        for attribute in (func for func in dir(self) if not func.startswith("__")):
            method = getattr(self, attribute, None)
            if callable(method) and hasattr(method, "validator"):
                method()

    def get_non_null_attributes(self) -> dict:
        """
        Construct a dictionary out of non-null keys (from attributes property)
        present on this object
        """

        def to_dict_compatible(value: Union[dict, list, object]) -> Union[dict, list]:
            if isinstance(value, list):
                return [to_dict_compatible(v) for v in value]
            else:
                to_dict = getattr(value, "to_dict", None)
                if to_dict and callable(to_dict):
                    return {
                        k: to_dict_compatible(v) for k, v in value.to_dict().items()
                    }
                else:
                    return value

        def is_not_empty(key: str) -> bool:
            value = getattr(self, key, None)
            if value is None:
                return False
            has_len = getattr(value, "__len__", None) is not None
            if has_len:
                return len(value) > 0
            else:
                return value is not None

        return {
            key: to_dict_compatible(getattr(self, key, None))
            for key in sorted(self.attributes)
            if is_not_empty(key)
        }

    def to_dict(self, *args) -> dict:
        """
        Extract this object as a JSON-compatible, Servicing-API-valid dictionary

        Args:
          *args: Any specific formatting args (rare; generally not required)

        Raises:
          ServicingObjectFormationError if the object was not valid
        """
        self.validate_json()
        return self.get_non_null_attributes()

    def __repr__(self):
        dict_value = self.get_non_null_attributes()
        if dict_value:
            return f"<servicing.{self.__class__.__name__}: {dict_value}>"
        else:
            return self.__str__()


class JsonValidator:
    def __init__(self, message: str):
        """
        Decorate a method on a class to mark it as a JSON validator. Validation
            functions should return true if valid, false if not.

        Args:
            message: Message to be attached to the thrown ServicingObjectFormationError
        """
        self.message = message

    def __call__(self, func: Callable) -> Callable[..., None]:
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            if not func(*args, **kwargs):
                raise ServicingObjectFormationError(self.message)

        wrapped_f.validator = True
        return wrapped_f


class EnumValidator(JsonValidator):
    def __init__(self, attribute: str, enum: Iterable[str]):
        super().__init__(
            f"{attribute} attribute must be one of the following values: "
            f"{', '.join(enum)}"
        )
