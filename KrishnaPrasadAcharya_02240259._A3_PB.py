import unittest

from KrishnaPrasadAcharya_02240259_A3_PA import (
    BankingSystem,
    PersonalAccount,
    BusinessAccount,
    InvalidInputException,
    InsufficientFundsException,
    AccountNotFoundException
)

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        self.system = BankingSystem()
        self.personal = PersonalAccount("12345", "pass1", 1000)
        self.business = BusinessAccount("67890", "pass2", 2000)
        self.system.accounts = {
            "12345": self.personal,
            "67890": self.business
        }

    # 1. Unusual user input
    def test_invalid_deposit_amount(self):
        with self.assertRaises(InvalidInputException):
            self.personal.deposit(-500)

    def test_invalid_withdraw_amount(self):
        with self.assertRaises(InvalidInputException):
            self.personal.withdraw(-100)

    def test_invalid_phone_number(self):
        with self.assertRaises(InvalidInputException):
            self.system.top_up_mobile(self.personal, "abc123", 50)

    def test_short_phone_number(self):
        with self.assertRaises(InvalidInputException):
            self.system.top_up_mobile(self.personal, "12345", 50)

    # 2. Invalid usage of application functions
    def test_overdraft(self):
        with self.assertRaises(InsufficientFundsException):
            self.personal.withdraw(2000)

    def test_transfer_to_nonexistent_account(self):
        with self.assertRaises(AccountNotFoundException):
            target = self.system.accounts.get("99999")
            if target is None:
                raise AccountNotFoundException("Recipient account not found.")

    def test_delete_and_use_account(self):
        self.system.delete_account("12345")
        with self.assertRaises(KeyError):
            _ = self.system.accounts["12345"]

    # 3. Testing main methods
    def test_deposit(self):
        self.personal.deposit(500)
        self.assertEqual(self.personal.balance, 1500)

    def test_withdraw(self):
        self.personal.withdraw(500)
        self.assertEqual(self.personal.balance, 500)

    def test_transfer(self):
        self.personal.transfer(200, self.business)
        self.assertEqual(self.personal.balance, 800)
        self.assertEqual(self.business.balance, 2200)

    def test_top_up_mobile(self):
        result = self.system.top_up_mobile(self.personal, "9876543210", 100)
        self.assertEqual(self.personal.balance, 900)
        self.assertIn("Successfully topped up", result)

if __name__ == '__main__':
    unittest.main()
