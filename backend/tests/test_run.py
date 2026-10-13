import unittest

from tests.unit.domain.User.test_created_at import TestCreatedAtValueObject
from tests.unit.domain.User.test_email import TestEmailValueObject
from tests.unit.domain.User.test_first_name import TestFirstNameValueObject
from tests.unit.domain.User.test_hash_password import TestRawPasswordRepresentation, TestRawPasswordValidation
from tests.unit.domain.User.test_last_name import TestLastNameValueObject
from tests.unit.domain.User.test_model import TestUserModel
from tests.unit.domain.User.test_username import TestUsernameValueObject
from tests.unit.infrastructure.database.test_query_builder import TestQueryBuilder
from tests.unit.infrastructure.database.test_unit_of_work import TestUnitOfWork

# from .integration.infrastructure.database.test_postgres_uow import TestPostgresUnitOfWorkIntegration

if __name__ == "__main__":
    suite = unittest.TestSuite()

    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestRawPasswordValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestRawPasswordRepresentation))
    suite.addTests(loader.loadTestsFromTestCase(TestFirstNameValueObject))
    suite.addTests(loader.loadTestsFromTestCase(TestLastNameValueObject))
    suite.addTests(loader.loadTestsFromTestCase(TestUsernameValueObject))
    suite.addTests(loader.loadTestsFromTestCase(TestCreatedAtValueObject))
    suite.addTests(loader.loadTestsFromTestCase(TestEmailValueObject))

    suite.addTests(loader.loadTestsFromTestCase(TestUserModel))

    suite.addTests(loader.loadTestsFromTestCase(TestUnitOfWork))
    suite.addTests(loader.loadTestsFromTestCase(TestQueryBuilder))

    # suite.addTests(loader.loadTestsFromTestCase(TestPostgresUnitOfWorkIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
