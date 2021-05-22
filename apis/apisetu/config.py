# Define all the constants being used by APISETU


HOST_URL = "https://cdn-api.co-vin.in/api"
STATE_URL = HOST_URL + "/v2/admin/location/states"
DISTRICT_URL = HOST_URL + "/v2/admin/location/districts/{state_id}"
APPOINTMENT_BY_DIST = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}"

APPOINTMENT_BY_PIN = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}'


APISETU_HEADERS = {
    "authority": "cdn-api.co-vin.in",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "origin": "https://www.cowin.gov.in",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.cowin.gov.in/",
    "accept-language": "en-US,en;q=0.9",
}


