from uuid import UUID

from servicing.util import is_uuid
from . import JsonObject, JsonValidator


class User(JsonObject):
    attributes = {"institution_id", "email"}

    def __init__(self, *, institution_id: UUID, email: str):
        self.institution_id = institution_id
        self.email = email

    @JsonValidator("institution_id attribute is required")
    def institution_id_present(self):
        return self.institution_id is not None

    @JsonValidator("institution_id attribute is not a valid UUID")
    def institution_id_is_uuid(self):
        return is_uuid(self.institution_id)

    @JsonValidator("email attribute is required")
    def email_present(self):
        return self.email is not None
