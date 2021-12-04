from alina.irena.client import IrenaClient
from alina.irena.factories import (
    IrenaTimetableAllocationsFactory, IrenaAllocationSignatureFactory, IrenaAllocationDetailsFactory,
    IrenaTripCrewMembersFactory
)


class Alina:
    """Init creates an instance of the class with the following parameters: username, password, and authenticate.
    These are passed to the constructor function which creates an instance of IrenaClient with these values
    as its parameters. The 'authenticate' parameter represents whether or not authentication was required when creating
    this object from IrenaClient(). If True, then authentication must have been performed before being able to create
    an instance of Alina using this constructor; otherwise, it can be left as False and there will be no need for
    any additional code.
    """

    def __init__(self, username, password, authenticate=True):
        self._client = IrenaClient(username, password, authenticate)

    def authenticate(self):
        return self._client.authenticate()

    def timetable_allocations(self, date):
        """Returns timetable which is actually a timetables list.
        Accepts date in pattern like: '2021-11-1'
        Returns list of dictionaries:
            {'title': 'KKA406', 'signature': '12691883693', 'date': '2021-11-01', 'start_hour': '16:32',
            'end_hour': '00:32'}
            {'title': 'KKA402', 'signature': '12691883701', 'date': '2021-11-03', 'start_hour': '23:22',
            'end_hour': '11:21'}
            {'title': 'KKA300', 'signature': '12691883694', 'date': '2021-11-05', 'start_hour': '06:15',
            'end_hour': '16:36'}
            {'title': 'KKA906', 'signature': '12715920193', 'date': '2021-11-07', 'start_hour': '13:21',
            'end_hour': '01:21'}
            {'title': 'KKA326', 'signature': '12691883702', 'date': '2021-11-10', 'start_hour': '12:08',
            'end_hour': '00:08'}
            {'title': 'KKA307', 'signature': '12691883695', 'date': '2021-11-11', 'start_hour': '12:08',
            'end_hour': '23:58'}
        """
        factory = IrenaTimetableAllocationsFactory(self._client, date)
        allocations = factory.produce()
        return allocations

    def allocation_signature(self, title, date):
        """Returns 'signature' of an allocation. Signature is required to search data like details of an timetables etc.
        Returns e.g. '12660988581'
        """
        factory = IrenaAllocationSignatureFactory(self._client, title, date)
        try:
            signature = factory.produce()
        except TypeError:
            return None
        else:
            return signature

    def allocation_details(self, title, date):
        """Returns details about an allocation.
        Returns list of dictionaries:
            {'train_number': '', 'action': 'DK Czas administracyjny', 'start_location': 'Katowice', 'start_hour':
            '07:57', 'end_location': 'Katowice', 'end_hour': '07:58'}
            {'train_number': '', 'action': 'DK Przyjęcie pociągu', 'start_location': 'Katowice', 'start_hour': '07:58',
            'end_location': 'Katowice', 'end_hour': '07:59'}
            {'train_number': '36102', 'action': 'IC Praca na pociągu.', 'start_location': 'Katowice', 'start_hour':
            '07:59', 'end_location': 'Jelenia Góra', 'end_hour': '13:41'}
            {'train_number': '', 'action': 'DK Zdanie pociągu', 'start_location': 'Jelenia Góra', 'start_hour': '13:41',
             'end_location': 'Jelenia Góra', 'end_hour': '13:47'}
            {'train_number': '', 'action': 'DK Zdanie pociągu', 'start_location': 'Jelenia Góra', 'start_hour': '13:47',
            'end_location': 'Jelenia Góra', 'end_hour': '13:47'}
            {'train_number': '', 'action': 'IC Płatna przerwa', 'start_location': 'Jelenia Góra', 'start_hour': '13:47',
             'end_location': 'Jelenia Góra', 'end_hour': '14:17'}
            {'train_number': '', 'action': 'DK Przyjęcie pociągu', 'start_location': 'Jelenia Góra', 'start_hour':
            '14:17', 'end_location': 'Jelenia Góra', 'end_hour': '14:20'}
            {'train_number': '63102', 'action': 'IC Praca na pociągu.', 'start_location': 'Jelenia Góra', 'start_hour':
            '14:20', 'end_location': 'Katowice', 'end_hour': '19:56'}
            {'train_number': '', 'action': 'DK Czas administracyjny', 'start_location': 'Katowice', 'start_hour':
            '19:56', 'end_location': 'Katowice', 'end_hour': '19:57'}
        """
        signature = self.allocation_signature(title, date)
        if not signature:
            return {}
        else:
            factory = IrenaAllocationDetailsFactory(self._client, signature, date)
            details = factory.produce()
            return details

    def train_crew(self, train_number, date):
        """ Returns train crew on a given date.
        Returns list of dictionaries:
            {'person': '...', 'phone_number': '838 382 932', 'profession': 'PM', 'start_location':
            '10:38 GDY_PO', 'end_location': '13:59 WWO'}
            {'person': '...', 'phone_number': '...', 'profession': 'M', 'start_location': '10:38 GDY_PO',
            'end_location': '13:56 WWO'}
        """
        factory = IrenaTripCrewMembersFactory(self._client, train_number, date)
        crew = factory.produce()
        return crew
