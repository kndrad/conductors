import re

from bs4 import BeautifulSoup, SoupStrainer

from IVU.api.requests import IVUTimetableAllocationsRegisterIDRequest, IVUAllocationRegisterComponentsRequest
from IVU.api.servers import IVUServer
from IVU.backends import get_credentials

id_regex = re.compile('(?P<id>\d+)')


def send_allocations_registers(request, date):
    username, password = get_credentials(request)

    server = IVUServer()
    server.login(username, password)

    request = IVUTimetableAllocationsRegisterIDRequest(date)
    response = server.send(request)

    strainer = SoupStrainer(
        name='table', class_='duties calendar-table'
    )
    soup = BeautifulSoup(markup=response.content, features='html.parser', parse_only=strainer)
    contents = soup.find_all(name='div', class_='allocation-container display-full')

    ids = []

    for container in contents:
        edition_element = container.find('div', class_='mdl-tooltip mdl-tooltip--large')

        if edition_element:
            if edition_element.text == 'Bez edycji':
                id = id_regex.search(container.find('div', class_='clickable').attrs['data-url'])['id']
                ids.append(id)

    for id in ids:
        request = IVUAllocationRegisterComponentsRequest(id)
        response = server.send(request)
        soup = BeautifulSoup(markup=response.content, features='html.parser')
        contents = soup.find_all(name='div', class_='component-content')

        components = []
        for i, content in enumerate(contents):
            attrs = {
                'class': 'mdl-menu mdl-menu--bottom-left mdl-js-menu',
                'for': f'components_{i}_type'
            }
            menu = content.find(name='ul', attrs=attrs)

            if menu:
                component = {}

                action_name = content.find(name='input', attrs={'id': f'components_{i}_type'})['data-saved']

                items = menu.find_all(name='li')
                for item in items:
                    if item.text == action_name:
                        component['dutyComponentTypeId'] = item['data-val']

                start_secs = content.find(name='input', attrs={'id': f'components_{i}_startTime'})['data-saved']
                component["startTimeSeconds"] = start_secs

                end_secs = content.find(name='input', attrs={'id': f'components_{i}_endTime'})['data-saved']
                component["endTimeSeconds"] = end_secs

                component["newlyCreated"] = "false"
                component["partNumber"] = "1"
                component["deleted"] = "false"
                component["comment"] = ""
                components.append(component)

        data = {"components": components, "comment": "", "allocatableId": id}
        return server.session.post(
            url='https://irena1.intercity.pl/mbweb/main/matter/desktop/json-actual-duty-submit', json=data
        )
