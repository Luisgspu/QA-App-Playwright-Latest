from App.vehicle_api import VehicleAPI
from App.XHRResponseCapturer import XHRResponseCapturer  # If this is in another file

TARGET_URL_FILTER = "https://daimleragemea.germany-2.evergage.com/"

def create_api_and_xhr(page):
    access_token = "your_api_access_token"
    vehicle_api = VehicleAPI(access_token)
    xhr_capturer = XHRResponseCapturer(page, TARGET_URL_FILTER, "")
    return vehicle_api, xhr_capturer