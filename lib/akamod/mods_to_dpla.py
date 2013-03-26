from akara import logger
from akara import request, response
from akara.services import simple_service
from amara.thirdparty import json
import base64

from dplaingestion.selector import getprop as selector_getprop, exists


def getprop(d, p):
    return selector_getprop(d, p, True)

CONTEXT = {
    "@vocab": "http://purl.org/dc/terms/",
    "dpla": "http://dp.la/terms/",
    "edm": "http://www.europeana.eu/schemas/edm/",
    "LCSH": "http://id.loc.gov/authorities/subjects",
    "name": "xsd:string",
    "collection" : "dpla:aggregation",
    "aggregatedDigitalResource" : "dpla:aggregatedDigitalResource",
    "originalRecord" : "dpla:originalRecord",
    "state": "dpla:state",
    "coordinates": "dpla:coordinates",
    "stateLocatedIn" : "dpla:stateLocatedIn",
    "sourceResource" : "edm:sourceResource",
    "dataProvider" : "edm:dataProvider",
    "hasView" : "edm:hasView",
    "isShownAt" : "edm:isShownAt",
    "object" : "edm:object",
    "provider" : "edm:provider",
    "begin" : {
        "@id" : "dpla:dateRangeStart",
        "@type": "xsd:date"
    },
    "end" : {
        "@id" : "dpla:dateRangeEnd",
        "@type": "xsd:date"
    }
}

def physical_description_handler(d, p):
    pd = getprop(d, p)
    out = {}
    pd = pd if isinstance(pd, list) else [pd]
    for _dict in pd:
        if "note" in _dict:
            note = getprop(_dict, "note")
            for sub_dict in note:
                if isinstance(sub_dict, dict) and "displayLabel" in sub_dict:
                    if sub_dict["displayLabel"] == "size inches":
                        out["extent"] = sub_dict.get("#text")
                    if sub_dict["displayLabel"] == "condition":
                        out["description"] = sub_dict.get("#text")
        if "form" in _dict:
            out["format"] = getprop(_dict, "form/#text")
    return out

def subject_handler(d, p):
    orig_subject = getprop(d, p)
    subjects = {"subject": []}
    for _dict in orig_subject:
        if "topic" in _dict:
            subjects["subject"].append(_dict["topic"])
        if "name" in _dict:
            subjects["subject"].append(getprop(_dict, "name/namePart"))
    return subjects

def get_media_type(d):
    pd = getprop(d, "physicalDescription")
    pd = pd if isinstance(pd, list) else [pd]
    for _dict in pd:
        try:
            return selector_getprop(_dict, "internetMediaType")
        except KeyError:
            pass

def location_handler(d, p):
    location = getprop(d, p)
    format = get_media_type(d)
    out = {}
    try:
        for _dict in location:
            if "url" in _dict:
                for url_dict in _dict["url"]:
                    if url_dict and "access" in url_dict:
                        if url_dict["access"] == "object in context":
                            out["isShownAt"] = url_dict.get("#text")
                        if url_dict["access"] == "preview":
                            out["object"] = url_dict.get("#text")
                        if url_dict["access"] == "raw object":
                            out["hasView"] = {"@id:": url_dict.get("#text"), "format": format}
            if "physicalLocation" in _dict and isinstance(_dict["physicalLocation"], basestring):
                out["dataProvider"] = _dict["physicalLocation"]
    except Exception as e:
        logger.error(e)
    finally:
        return out

def creator_handler_uva(d, p):
    creator_dict = getprop(d, p)
    if isinstance(creator_dict, dict) and "type" in creator_dict and "namePart" in creator_dict:
        if creator_dict["type"] == "personal":
            parsed = []
            for name_part in creator_dict["namePart"]:
                # preserve parsing order
                if name_part["type"] == "given":
                    parsed.append(name_part.get("#text"))
                if name_part["type"] == "family":
                    parsed.append(name_part.get("#text"))
                if name_part["type"] == "date":
                    parsed.append(name_part.get("#text"))
            return {"creator": ", ".join(parsed)}
        if creator_dict["type"] == "corporate":
            return {"creator": creator_dict["namePart"]}

def creator_handler_nypl(d, p):
    creator_roles = frozenset(("architect", "artist", "author", "cartographer",
                     "composer", "creator", "designer", "director",
                     "engraver", "interviewer", "landscape architect",
                     "lithographer", "lyricist", "musical director",
                     "performer", "project director", "singer", "storyteller",
                     "surveyor", "technical director", "woodcutter"))
    creator_dict = getprop(d, p)
    out = {}
    if isinstance(creator_dict, dict) and "type" in creator_dict and "namePart" in creator_dict:
        if creator_dict["type"] == "personal" and exists(creator_dict, "role/roleTerm"):
            roles = frozenset([role_dict["#text"].lower() for role_dict in creator_dict["role"]["roleTerm"] if "#text" in role_dict])
            name = creator_dict["namePart"]
            if "publisher" not in roles:
                out["contributor"] = name
            else:
                out["publisher"] = name
            if roles.issubset(creator_roles):
                out["creator"] = name
    return out


CHO_TRANSFORMER = {"3.3": {}, "3.4": {}, "common": {}}
AGGREGATION_TRANSFORMER = {"3.3": {}, "3.4": {}, "common": {}}

# Structure mapping the original property to a function returning a single
# item dict representing the new property and its value
CHO_TRANSFORMER["3.3"] = {
    "recordInfo/languageOfCataloging/languageTerm/#text": lambda d, p: {"language": getprop(d, p)},
    "name": creator_handler_uva,
    "physicalDescription": physical_description_handler,
    "originInfo/place/placeTerm": lambda d, p: {"spatial": getprop(d, p)},
    "accessCondition": lambda d, p: {"rights": [s["#text"] for s in getprop(d, p) if "#text" in s]},
    "subject": subject_handler,
    "titleInfo/title": lambda d, p: {"title": getprop(d, p)},
    "typeOfResource/#text": lambda d, p: {"type": getprop(d, p)},
    "originInfo/dateCreated/#text": lambda d, p: {"date": getprop(d, p)},
    "identifier": lambda d, p: {"identifier": "-".join(s.get("#text") for s in getprop(d, p) if s["type"] == "uri")}
}

CHO_TRANSFORMER["3.4"] = {
    "name": creator_handler_nypl,
    "physicalDescription": physical_description_handler,
    "identifier": lambda d, p: {"identifier": [s.get("#text") for s in getprop(d, p) if s["type"] in ("local_bnumber", "uuid")]},
    "relatedItem/titleInfo/title": lambda d, p: {"isPartOf": getprop(d, p)},
    "typeOfResource": lambda d, p: {"type": getprop(d, p)},
    "titleInfo": lambda d, p: {"title": [s.get("title") for s in getprop(d, p) if s.get("usage") == "primary" and s.get("supplied") == "no"]},
}


AGGREGATION_TRANSFORMER["common"] = {
    "id"                         : lambda d, p: {"id": getprop(d, p), "@id" : "http://dp.la/api/items/" + getprop(d, p)},
    "_id"                        : lambda d, p: {"_id": getprop(d, p)},
    "originalRecord"             : lambda d, p: {"originalRecord": getprop(d, p)},
    "collection"                 : lambda d, p: {"collection": getprop(d, p)},
    "ingestType"                 : lambda d, p: {"ingestType": getprop(d, p)},
    "ingestDate"                 : lambda d, p: {"ingestDate": getprop(d, p)}
}

AGGREGATION_TRANSFORMER["3.3"] = {
    "location": location_handler,
    "recordInfo/recordContentSource": lambda d, p: {"provider": getprop(d, p)}
}

@simple_service('POST', 'http://purl.org/la/dp/mods-to-dpla', 'mods-to-dpla', 'application/ld+json')
def mods_to_dpla(body, ctype, geoprop=None, version=None):
    """
    Convert output of JSON-ified MODS/METS format into the DPLA JSON-LD format.

    Parameter "geoprop" specifies the property name containing lat/long coords

    Parameter "version" specifies the mapping dictionary, None means autodetect try,
    corresponds to MODS format version
    """

    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"

    global GEOPROP
    GEOPROP = geoprop

    out = {
        "@context": CONTEXT,
        "sourceResource" : {}
    }

    if not version:
        version = getprop(data, "version")

    # Apply all transformation rules from original document
    transformer_pipeline = {}
    transformer_pipeline.update(CHO_TRANSFORMER.get(version, {}), **CHO_TRANSFORMER["common"])
    for p in transformer_pipeline:
        if exists(data, p):
            out["sourceResource"].update(transformer_pipeline[p](data, p))
    transformer_pipeline = {}
    transformer_pipeline.update(AGGREGATION_TRANSFORMER.get(version, {}), **AGGREGATION_TRANSFORMER["common"])
    for p in transformer_pipeline:
        if exists(data, p):
            out.update(transformer_pipeline[p](data, p))

    # Additional content not from original document
    if 'HTTP_CONTRIBUTOR' in request.environ:
        try:
            out["provider"] = json.loads(base64.b64decode(request.environ['HTTP_CONTRIBUTOR']))
        except Exception as e:
            logger.debug("Unable to decode Contributor header value: "+request.environ['HTTP_CONTRIBUTOR']+"---"+repr(e))

    # Strip out keys with None/null values?
    out = dict((k,v) for (k,v) in out.items() if v)

    return json.dumps(out)
