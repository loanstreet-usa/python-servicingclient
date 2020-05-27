from typing import Optional

from . import JsonObject, JsonValidator


class Address(JsonObject):
    attributes = {"street_one", "street_two", "city", "state", "zip"}

    def __init__(
        self, *, street_one: str, street_two: str, city: str, state: str, zip: str
    ):
        self.street_one = street_one
        self.street_two = street_two
        self.city = city
        self.state = state
        self.zip = zip

    @JsonValidator("street_one attribute is required")
    def street_one_present(self):
        return self.street_one is not None

    @JsonValidator("city attribute is required")
    def city_present(self):
        return self.city is not None

    @JsonValidator("state attribute is required")
    def state_present(self):
        return self.state is not None

    @JsonValidator("zip attribute is required")
    def zip_present(self):
        return self.zip is not None


class Institution(JsonObject):
    attributes = {"name", "ticker", "address"}

    def __init__(
        self,
        *,
        name: str,
        ticker: Optional[str] = None,
        address: Optional[Address] = None
    ):
        self.name = name
        self.ticker = ticker
        self.address = address

    @JsonValidator("name attribute is required")
    def name_present(self):
        return self.name is not None
