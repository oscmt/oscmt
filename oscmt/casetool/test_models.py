from django.test import TestCase
from datetime import date

from casetool.models import *

class ClientTestCase(TestCase):
    def setUp(self):
        Client.objects.create(
            name = 'clientname'
        )

    def test_client_has_a_name(self):
        """A Client must have a Name"""

        client = Client.objects.get(
            name = 'clientname'
        )

        self.assertEqual(client.name, 'clientname')

class ConsultantTestCase(TestCase):
    def setUp(self):
        Consultant.objects.create(
            first_name = 'consultantfirstname',
            last_name = 'consultantlastname'
        )

    def testConsultantHasAFirstName(self):
        """A Consultant must have a First Name"""

        consultant = Consultant.objects.get(
            first_name = 'consultantfirstname'
        )

        self.assertEqual(consultant.first_name, 'consultantfirstname')

    def test_Consultant_has_a_last_name(self):
        """A Consultant must have a Last Name"""
        consultant = Consultant.objects.get(
            last_name = 'consultantlastname'
        )

        self.assertEqual(consultant.last_name, 'consultantlastname')

class ContactTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(
            first_name = 'contactfirstname',
            last_name = 'contactlastname',
            phone_number = '0711-123456',
            email_address = 'contactfirstname.contactlastname@contactcompany.com',
            company = 'contactcompany'
        )

    def test_contact_has_a_first_name(self):
        """A Contact must have a First Name"""

        contact = Contact.objects.get(
            first_name = 'contactfirstname'
        )

        self.assertEqual(contact.first_name, 'contactfirstname')

    def test_contact_has_a_last_name(self):
        """A Contact must have a Last Name"""

        contact = Contact.objects.get(
            last_name = 'contactlastname'
        )

        self.assertEqual(contact.last_name, 'contactlastname')

class ContractTestCase(TestCase):
    def setUp(self):
        # create needed objects
        Client.objects.create(
            name = 'clientname'
        )

        client = Client.objects.get(
            name = 'clientname'
        )
        start = date(2016, 8, 1)
        end = date(2016, 8, 2)
        cost_limit = 1
        time_limit = 1

        Contract.objects.create(
            client = client,
            start = start,
            end = end,
            cost_limit = cost_limit,
            time_limit = time_limit,
        )

    def test_contract_has_a_client(self):
        client = Client.objects.get(
            name = 'clientname'
        )
        contract = Contract.objects.get(
            client = client
        )

        self.assertEqual(contract.client, client)

class CaseTestCase(TestCase):
    def setUp(self):
        # create needed objects
        Client.objects.create(
            name = 'clientname'
        )

        Consultant.objects.create(
            first_name = 'consultantfirstname',
            last_name = 'consultantlastname'
        )

        Contact.objects.create(
            first_name = 'contactfirstname',
            last_name = 'contactlastname',
            phone_number = '0711-123456',
            email_address = 'contactfirstname.contactlastname@contactcompany.com',
            company = 'contactcompany'
        )

        client = Client.objects.get(
            name = 'clientname'
        )
        start = date(2016, 8, 1)
        end = date(2016, 8, 2)
        cost_limit = 1
        time_limit = 1

        Contract.objects.create(
            client = client,
            start = start,
            end = end,
            cost_limit = cost_limit,
            time_limit = time_limit,
        )

        # query for needed objects
        consultant = Consultant.objects.get(
            last_name = 'consultantlastname'
        )

        contact = Contact.objects.get(
            first_name = 'contactfirstname',
        )

        client = Client.objects.get(
            name = 'clientname'
        )

        contract = Contract.objects.get(
            client = client
        )

        # create case objects for testcase
        Case.objects.create(
            external_id = 'testcase',
            internal_main_contact = consultant,
            external_main_contact = contact,
            client = client,
            contract = contract,
        )

        Case.objects.create(
            external_id = 'testcase2',
            internal_main_contact = consultant,
            external_main_contact = contact,
            client = client,
            contract = contract,
        )


    def test_case_has_a_client(self):
        """A Case must have a Client"""
        case = Case.objects.get(external_id = 'testcase')
        self.assertEqual(case.client.name, 'clientname')

    def test_case_has_analysis_storage(self):
        """A Case must have an Analysis Storage corresponding to the external_id"""
        case = Case.objects.get(external_id = 'testcase')
        self.assertEqual(case.analysis_storage, '/vmpool/testcase')

    def test_case_done_sets_deletion_date(self):
        """If case done is newly set to true, a deletion date must be set dynamically to today + 0.5years"""
        import datetime
        deletion_date = (datetime.date.today() + datetime.timedelta(6*365/12))
        case = Case.objects.get(external_id = 'testcase')
        case.case_done = True
        case.save()
        self.assertEqual(case.deletion_date, deletion_date)

#    def test_case_deletion_date_is_readonly(self):
#        """If a deletion date is set by case_done, it must not be writable"""
#        import datetime
#        deletion_date = (datetime.date.today() + datetime.timedelta(6*365/12))
#        overwrite_date = datetime.date.today()
#        case = Case.objects.get(external_id = 'testcase')
#        case.case_done = True
#        case.save()
#        case.deletion_date = overwrite_date
#        self.assertEqual(case.deletion_date, deletion_date)
#        self.assertNotEqual(case.deletion_date, overwrite_date)

    def test_case_consecutive_number_generator_works_with_zero_previous_cases(self):
        """If previously in the year no cases were stored the first generated number should be 1"""
        case = Case.objects.get(external_id='testcase')
        self.assertEqual(case.consecutive_number, 1)

    def test_case_consecutive_number_generator_correctly_increments_number(self):
        """If a previous case was stored, the consecutive_number field should be incremented"""
        case = Case.objects.get(external_id = 'testcase2')
        self.assertEqual(case.consecutive_number, 2)

    def tearDown(self):
        """cleaning up after the test, especially the created files"""
        import subprocess
        subprocess.call(['rm', '-r', '/vmpool/testcase'])
        subprocess.call(['rm', '-r', '/vmpool/testcase2'])
