from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json
from dplaingestion.selector import getprop, setprop, exists
from dplaingestion.utilities import iterify
import re

@simple_service("POST", "http://purl.org/la/dp/texas_enrich_location",
                "texas_enrich_location", "application/json")
def texas_enrich_location(body, ctype, action="texas_enrich_location",
                          prop="sourceResource/spatial"):
    """
    Service that accepts a JSON document and enriches the "spatial" field of
    that document.

    For use with the texas profile
    """

    try:
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header("content-type", "text/plain")
        return "Unable to parse body as JSON"


    def _get_coordinates(values):
        lat, lon = None, None
        for v in values:
            if "north=" in v:
                lat = v.split("=")[-1]
            elif "east=" in v:
                lon = v.split("=")[-1]

        if lat and lon:
            return (lat, lon)
        else:
            return ()

    if exists(data, prop):
        spatial = []
        values = getprop(data,prop)

        for i in range(len(values)):
            sp = {}
            if " - " in values[i]:
                values[i] = [s.strip() for s in values[i].split(" - ")]
            elif ";" in values[i]: 
                values[i] = [s.strip() for s in values[i].split(";")]
            else:
                values[i] = [values[i]]

            coordinates = _get_coordinates(values[i]) 
            if coordinates:
                sp["name"] = "%s, %s" % coordinates
            else:
                sp["name"] = " ".join(values[i])

            if len(values[i]) < 5:
                if not re.search("\d", sp["name"]):
                    sp["country"] = values[i][0]
                if "country" in sp:
                    if sp["country"] == "United States":
                        try:
                            sp["state"] = values[i][1]
                            sp["county"] = values[i][2]
                            sp["city"] = values[i][3]
                        except Exception, e:
                            logger.debug("Error enriching location %s: %s" %
                                         (data["_id"], e))
                    elif sp["country"] == "Canada":
                        try:
                            sp["provence"] = values[i][1]
                            sp["city"] = values[i][2]
                        except Exception, e:
                            logger.debug("Error enriching location %s: %s" %
                                         (data["_id"], e))
            spatial.append(sp)
        logger.debug("SPATIAL: %s" % spatial)
        setprop(data, prop, spatial)

    return json.dumps(data)

def replace_state_abbreviations(name):
    """
    Replace abbreviations used in SCDL data with more common versions.
    """
    ABBREV = {
        "(Ala.)": "AL",
        "(Calif.)": "CA",
        "(Conn.)": "CT",
        "(Ill.)": "IL",
        "(Mass.)": "MA",
        "(Miss.)": "MS",
        "(Tex.)": "TX",
        "(Wash.)": "WA",
    }
    for abbrev in ABBREV: 
        if (abbrev in name): 
            return name.replace(abbrev, ABBREV[abbrev])
    return name
