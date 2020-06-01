from uuid import UUID
import unittest
from servicing.web.classes.user import User


class UserTests(unittest.TestCase):
    def test_json(self):
        institution_id = UUID("b5ba849f-6975-4e90-b2e4-fbdec3514a68")
        self.assertDictEqual(
            User(
                institution_id=institution_id,
                email="test@loan-street.com"

            ).to_dict(),
            {
                "institution_id": institution_id,
                "email": "test@loan-street.com"
            }
        )
