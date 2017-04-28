from park_api.util import convert_date
from park_api.geodata import GeoData
from datetime import datetime
import json
import re

# This loads the geodata for this city if <city>.geojson exists in the same directory as this file.
geodata = GeoData(__file__)


def parse_html(raw_json):

    data_as_json = json.loads(raw_json)
    data_as_json = data_as_json["data"]

    #TODO make the parser for the date working
    last_updated = data_as_json["updated"]
    last_updated = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    data = {
        "last_updated": convert_date(last_updated, "%Y/%m/%d %H:%M:%S"),
        "lots": []
    }

    state_mappings = {
        0: "open",
        1: "closed"
    }

    for record in data_as_json["parkinglocations"]:
        lot_name = record["name"]
        parking_info = record["parkingupdate"]
        free = int(parking_info["total"]) - int(parking_info["current"])
        total = int(parking_info["total"])

        print(lot_name)
        print(str(total) + " / " + str(free))

        # the JSON file contains parking lots for which counting does work, let's ignore them
        if total > 0:
            state_key = int(record["is_closed"])
            state = state_mappings[state_key]
            #TODO collect geodata -> GeoJSON
        #     lot = geodata.lot(lot_name)
            data["lots"].append({
                "name": lot_name,
                "free": free,
                "total": total,
                # "address": lot.address,
                # "coords": lot.coords,
                "state": state,
                # "lot_type": lot.type,
                # "id": lot.id,
                "forecast": False
            })



    return data
