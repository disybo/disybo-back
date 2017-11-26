""" Global configurations and static data"""

# Stara API and endpoints (https://documenter.getpostman.com/view/1976410/stara/6tc44mC#intro)
STARA_API_BASE = "https://dev-stara.elisaiot.com/Thingworx/Things/Stara/Services"
STARA_ENDPOINTS = {
    'vehicles': "{}/Vehicles".format(STARA_API_BASE),
    'refuel_events': "{}/Refuel".format(STARA_API_BASE),
    'vehicle_loc': "{}/Location".format(STARA_API_BASE),
    'garage_info': "{}/Garage".format(STARA_API_BASE),
    'garage_by_vehicle': "{}/GarageByVehicle".format(STARA_API_BASE),
    'garage_by_sehiid': "{}/GarageBySEHIID".format(STARA_API_BASE)
}
