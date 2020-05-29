from . import JsonObject, JsonValidator


class Fund(JsonObject):
    attributes = {"name"}

    def __init__(self, *, name: str):
        self.name = name

    @JsonValidator("name is required")
    def name_present(self):
        return self.name is not None
