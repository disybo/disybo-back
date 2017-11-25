""" Global configurations and static data"""

# Stara API and endpoints (https://documenter.getpostman.com/view/1976410/stara/6tc44mC#intro)
StaraAPI = {}
StaraAPI.endpoints = {}
StaraAPI.base = "https://dev-stara.elisaiot.com/Thingworx/Things/Stara/Services/"
StaraAPI.endpoints.vehicles = "{}/Vehicles".format(StaraAPI.base)
StaraAPI.endpoints.refuel_events = "{}/Refuel".format(StaraAPI.base)
StaraAPI.endpoints.vehicle_loc = "{}/Location".format(StaraAPI.base)
StaraAPI.endpoints.garage_info = "{}/Garage".format(StaraAPI.base)
StaraAPI.endpoints.garage_by_vehicle = "{}/GarageByVehicle".format(StaraAPI.base)
StaraAPI.endpoints.garage_by_sehiid = "{}/GarageBySEHIID".format(StaraAPI.base)
