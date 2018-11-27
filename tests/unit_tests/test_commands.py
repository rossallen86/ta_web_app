import unittest as ut
from ta_app.commands import Commands
import ta_app.wsgi
from website.models import Account, Course


class TestCommands(ut.TestCase):

    def setUp(self):
        self.ui = Commands()
        self.tst_supervisor = Account(user='usrSupervisor', password='password', role='Supervisor')
        self.tst_administrator = Account(user='usrAdministrator', password='password', role='Administrator')
        self.tst_instructor = Account(user='usrInstructor', password='password', role='Instructor')
        self.tst_ta = Account(user='usrTA', password='password', role='TA')
        self.tst_supervisor.save()
        self.tst_administrator.save()
        self.tst_instructor.save()
        self.tst_ta.save()

        self.test_accounts = []
        self.test_accounts.append(self.tst_supervisor)
        self.test_accounts.append(self.tst_administrator)
        self.test_accounts.append(self.tst_instructor)
        self.test_accounts.append(self.tst_ta)

    def tearDown(self):
        for i in self.test_accounts:
            i.delete()

    def testCallCommandValid(self):
        expected_output = 'login\nhelp\n'
        actual_output = self.ui.call_command('help')
        self.assertEqual(expected_output, actual_output)

    def testCallCommandInvalid(self):
        expected_output = 'ERROR: this is not an available command'
        actual_output = self.ui.call_command('invalidCommand')
        self.assertEqual(expected_output, actual_output)

    def test_help_with_no_current_user(self):
        self.ui.current_user = Account()
        expected_output = 'login\nhelp\n'
        actual_output = self.ui.call_command('help')
        self.assertEqual(expected_output, actual_output)

    def test_login_bad_username(self):
        self.ui.current_user = Account()
        username = 'badUsername'
        expected_output = 'login failed! bad username/ password'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertNotEqual(self.ui.current_user.user, username)
        self.assertTrue(self.ui.current_user.id is None)

    def test_login_bad_password(self):
        self.ui.current_user = Account()
        username = 'usrSupervisor'
        expected_output = 'login failed! bad username/ password'
        actual_output = self.ui.login(username, 'badPassword')
        self.assertEqual(expected_output, actual_output)
        self.assertNotEqual(self.ui.current_user.user, username)
        self.assertTrue(self.ui.current_user.id is None)

    def test_login_supervisor(self):
        self.ui.current_user = Account()
        username = 'usrSupervisor'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_supervisor)

        commands = self.ui.command_list
        expected_num_commands = 13
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('delete_account'))
        self.assertTrue(commands.__contains__('edit_account'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('assign_instructor'))
        self.assertTrue(commands.__contains__('assign_ta_to_course'))
        self.assertTrue(commands.__contains__('assign_ta_to_lab'))
        self.assertTrue(commands.__contains__('view_course_assignments'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_login_administrator(self):
        self.ui.current_user = Account()
        username = 'usrAdministrator'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_administrator)

        commands = self.ui.command_list
        expected_num_commands = 10
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('delete_account'))
        self.assertTrue(commands.__contains__('edit_account'))
        self.assertTrue(commands.__contains__('create_account'))
        self.assertTrue(commands.__contains__('view_course_assignments'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_login_instructor(self):
        self.ui.current_user = Account()
        username = 'usrInstructor'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_instructor)

        commands = self.ui.command_list
        expected_num_commands = 7
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('assign_ta_to_lab'))
        self.assertTrue(commands.__contains__('view_course_assignments'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_login_ta(self):
        self.ui.current_user = Account()
        username = 'usrTA'
        expected_output = 'login successful...'
        actual_output = self.ui.login(username, 'password')
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(self.ui.get_current_user(), self.tst_ta)

        commands = self.ui.command_list
        expected_num_commands = 5
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('logout'))
        self.assertTrue(commands.__contains__('view_ta_assignments'))
        self.assertTrue(commands.__contains__('edit_contact_info'))
        self.assertTrue(commands.__contains__('read_contact_info'))
        self.assertTrue(commands.__contains__('help'))

    def test_logout(self):
        self.ui.login('usrSupervisor', 'password')
        expected_output = 'logout successful...'
        actual_output = self.ui.logout()
        self.assertEqual(expected_output, actual_output)
        self.assertIsNone(self.ui.get_current_user().id)

        commands = self.ui.command_list
        expected_num_commands = 2
        self.assertEqual(expected_num_commands, len(commands))
        self.assertTrue(commands.__contains__('login'))
        self.assertTrue(commands.__contains__('help'))

    def test_create_account_as_supervisor(self):
        self.ui.login('usrSupervisor', 'password')
        username = 'tstCreatSupervisor'
        password = 'password'
        role = 'Supervisor'
        expected_output = 'Successfully created account'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.test_accounts.append(created_account)
        self.assertIsNotNone(created_account.id)
        self.assertEqual(created_account.user, username)
        self.assertEqual(created_account.password, password)
        self.assertEqual(created_account.role, role)

    def test_create_account_as_administrator_(self):
        self.ui.login('usrAdministrator', 'password')
        username = 'tstCreatSupervisor'
        password = 'password'
        role = 'TA'
        expected_output = 'Successfully created account'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.test_accounts.append(created_account)
        self.assertIsNotNone(created_account.id)
        self.assertEqual(created_account.user, username)
        self.assertEqual(created_account.password, password)
        self.assertEqual(created_account.role, role)

    def test_create_supervisor_account_as_administrator(self):
        self.ui.login('usrAdministrator', 'password')
        username = 'tstCreatSupervisorAsAdmin'
        password = 'password'
        role = 'Supervisor'
        expected_output = 'Failed to create account. Insufficient permissions'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.assertIsNone(created_account.id)

    def test_create_account_as_instructor(self):
        self.ui.login('usrInstructor', 'password')
        username = 'tstCreatTA'
        password = 'password'
        role = 'TA'
        expected_output = 'Failed to create account. Insufficient permissions'
        actual_output = self.ui.create_account(username, password, role)
        self.assertEqual(expected_output, actual_output)
        created_account = self.ui.get_account(username)
        self.assertIsNone(created_account.id)

    def test_create_account_as_ta(self):
        self.ui.login('usrTA', 'password')
        username = 'tstCreatTA'
        password = 'password'
        role = 'TA'
        initial_count = Account.objects.count()
        expected_output = 'Failed to create account. Insufficient permissions'
        actual_output = self.ui.create_account(username, password, role)
        final_count = Account.objects.count()
        created_account = self.ui.get_account(username)
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)
        self.assertIsNone(created_account.id)

    def test_create_account_existing_user(self):
        self.ui.login('usrSupervisor', 'password')
        username = 'usrTA'
        password = 'password'
        role = 'TA'
        expected_output = 'Failed to create account. User already exists'
        initial_count = Account.objects.count()
        actual_output = self.ui.create_account(username, password, role)
        final_count = Account.objects.count()
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(initial_count, final_count)

    def test_delete_account_as_supervisor(self):
        pass