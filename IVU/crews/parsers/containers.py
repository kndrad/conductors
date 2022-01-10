from IVU.abstracts.parsers.containers import IVUContainerHTML


class IVUTripCrewMemberContainerHTML(IVUContainerHTML):
    name = 'div'
    attrs = {'class': 'crew-value'}

    def _get_column_value(self, name):
        attrs = {
            'class': 'crew-info-column',
            'title': name,
        }
        column = self.markup.find('li', attrs=attrs)
        value = column.find('span')
        return value

    def _get_person(self):
        name = self._get_column_value('Nazwa')
        return name.text

    def _get_phone_number(self):
        try:
            number = self._get_column_value('Numer telefonu')
        except AttributeError:
            return None
        else:
            return number.text

    def _get_profession(self):
        profession = self._get_column_value('Typ załogi')
        return profession.text

    def _get_location(self, location):
        location = self._get_column_value(location)
        return location.text

    def to_dict(self):
        try:
            return {
                'person': self._get_person().title(),
                'phone': self._get_phone_number(),
                'profession': self._get_profession(),
                'start_location': self._get_location('Lokalizacja początkowa i początkowa'),
                'end_location': self._get_location('Koniec i cel'),
            }
        except AttributeError:
            return