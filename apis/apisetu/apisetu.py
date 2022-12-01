import requests
from datetime import datetime
from .config import *
from .objects import *
import json
from django.conf import settings

base_file_path = settings.BASE_DIR / 'apis/apisetu/mock_response'
def read_json(file_name):
    file_path = "{}/{}".format(base_file_path, file_name)
    with open(file_path, "r") as f:
        data = json.loads(f.read())
    return data


class ApiSetu:
    def __init__(self):
        pass

    def _send_request(self, url, response_file_name=None):
        # response_file_name is name of mocked response file.
        response = requests.request("GET", url, headers=APISETU_HEADERS, data={})

        # Uncomment below 2 lines if you think API's are not working as expected.
        # Below line will return the presaved response
        # if response_file_name:
        #     return read_json(response_file_name)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request Failed. Error {response.text}")

    def _get_date(self):
        date = datetime.today().date()
        return date.strftime('%d-%m-%Y')

    def get_states(self):
        """
        Returns the list of states from Apisetu.org
        :return:
        """
        # url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
        url = STATE_URL
        data = self._send_request(url, 'states.json')
        resp = [StateObject(**state) for state in data.get('states')]
        return resp

    def get_districts(self, state_id):
        url = DISTRICT_URL.format(state_id=state_id)
        data = self._send_request(url, 'districts.json')
        resp = [DistrictObject(**d) for d in data.get('districts')]
        return resp

    def get_appointments_by_district(self, district_id, date=None ):
        # Date=01-05-2021
        if not date:
            date = self._get_date()
        url = APPOINTMENT_BY_DIST.format(district_id=district_id, date=date)
        data = self._send_request(url,'app_by_district.json')
        resp = [CenterObject(**d) for d in data.get('centers')]
        return resp
    def get_appointments_by_pincode(self, pincode, date=None ):
        if not date:
            date = self._get_date()
        url = APPOINTMENT_BY_PIN.format(pincode=pincode, date=date)
        data = self._send_request(url, 'app_by_pincode.json')
        resp = [CenterObject(**d) for d in data.get('centers')]
        return resp
