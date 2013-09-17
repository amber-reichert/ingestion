from akara import logger
from akara import request, response
from akara.services import simple_service
from amara.lib.iri import is_absolute
from amara.thirdparty import json
from functools import partial
import base64
import sys
import re
from copy import deepcopy
from dplaingestion.selector import getprop, exists
from dplaingestion.utilities import remove_key_prefix, iterify

GEOPROP = None
META = "metadata/metadata/"

#FIXME not format specific, move to generic module
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
     "@id" : "dpla:end",
     "@type": "xsd:date"
   }
}

RIGHTS_TERM_LABEL = {
    "by": "Attribution.",
    "by-nc": "Attribution Noncommercial.",
    "by-nc-nd": "Attribution Non-commercial No Derivatives.",
    "by-nc-sa": "Attribution Noncommercial Share Alike.",
    "by-nd": "Attribution No Derivatives.",
    "by-sa": "Attribution Share Alike.",
    "copyright": "Copyright.",
    "pd": "Public Domain."
}

def rights_transform(d, p):
    rights = None
    license = None
    statement = None
    for s in iterify(getprop(d, p)):
        qualifier = s.get("qualifier")
        
        if qualifier == "license":
            try:
                license = "License: " + RIGHTS_TERM_LABEL[s.get("#text")]
            except:
                logger.error("Term %s not in RIGHTS_TERM_LABEL for %s" %
                             (s.get("#text"), d["_id"]))
        elif qualifier == "statement":
            statement = s.get("#text")

    if statement is not None and license is None:
        logger.debug("Statement without license for records %s" % d["_id"])

    if license is not None:
        rights = license
        if statement is not None:
            rights += "; " + statement

    return {"rights": rights} if rights else {}

def identifier_transform(d, p):
    identifier = []
    for s in iterify(getprop(d, p)):
        if "qualifier" in s and "#text" in s:
            identifier.append("%s: %s" % (s["qualifier"], s["#text"]))

    # Add rights values as well
    rights = getprop(d, META + "rights", True)
    if rights is not None:
        for s in iterify(rights):
            if "qualifier" in s and "#text" in s:
                identifier.append("%s: %s" % (s["qualifier"], s["#text"]))
    else:
        logger.debug("RIGHTS: none for %s" % d["_id"])

    return {"identifier": identifier} if identifier else {}

def spatial_transform(d, p):
    spatial = []
    for s in iterify(getprop(d, p)):
        if isinstance(s, basestring):
            spatial.append(s)
            logger.debug("SPATIAL: string for %s" % d["_id"])
        elif s.get("qualifier") in ["placeName", "placePoint", "placeBox"]:
            spatial.append(s.get("#text"))

    return {"spatial": spatial} if spatial else {}

def publisher_transform(d, p):
    publisher = []
    for s in iterify(getprop(d, p)):
        if "location" in s and "name" in s:
            publisher.append("%s: %s" % (s["location"], s["name"]))

    return {"publisher": publisher} if publisher else {}

def spectype_and_format_transform(d, p):
    return {}

def description_transform(d, p):
    description = []
    for s in iterify(getprop(d, p)):
        if isinstance(s, basestring):
            description.append(s)
        else:
            description.append(s.get("#text"))
    description = filter(None, description)

    return {"description": description} if description else {}

def creator_transform(d, p):
    creator = []
    for s in iterify(getprop(d, p)):
        if isinstance(s, basestring):
            creator.append(s)
        else:
            creator.append(s.get("name"))
    creator = filter(None, creator)

    return {"creator": creator} if creator else {}

def title_transform(d, p):
    title = []
    for s in iterify(getprop(d, p)):
        if isinstance(s, basestring):
            title.append(s)
        else:
            title.append(s.get("#text"))
    title = filter(None, title)

    return {"title": title} if title else {}

def subject_transform(d, p):
    subject = []
    for s in iterify(getprop(d, p)):
        if isinstance(s, basestring):
            subject.append(s)
        else:
            subject.append(s.get("#text"))
    subject = filter(None, subject)

    return {"subject": subject} if subject else {}

def date_transform(d, p):
    date = []
    for s in iterify(getprop(d, p)):
        if isinstance(s, basestring):
            logger.debug("DATE: basestring %s for %s" % (s, d["_id"]))
        elif s.get("qualifier") == "creation":
            date.append(s.get("#text"))

    # Get dates from coverage
    coverage = getprop(d, META + "coverage", True)
    if coverage is not None:
        start = None
        end = None
        for s in iterify(coverage):
            if not isinstance(s, basestring):
                qualifier = s.get("qualifier")
                text = s.get("#text")
                if qualifier == "sDate":
                    start = text
                elif qualifier == "eDate":
                    end = text
        if start is not None and end is not None:
            date.append("%s-%s" % (start, end))
    else:
        logger.debug("COVERAGE: none for %s" % d["_id"])

    return {"date": date} if date else {}

def url_transform(d, p):
    urls = {}
    for s in iterify(getprop(d, p)):
        qualifier = s.get("qualifier")
        text = s.get("#text")
        if qualifier == "itemURL":
            urls["isShownAt"] = text
        elif qualifier == "thumbnailURL":
            urls["object"] = text

    return urls

def spectype_and_format_transforms(d, p):
    spectype_and_format = {}
    spectype = None
    for s in iterify(getprop(d, p)):
        values = s.split("_")
        spectype_and_format["format"] = values[0]
        try:
            if values[1] in ["book", "newspaper", "journal"]:
                spectype = values[1]
            elif values[1] == "leg":
                spectype = "government document"
            elif values[1] == "serial":
                spectype = "journal"
        except:
            pass
    if spectype is not None:
        spectype_and_format["specType"] = spectype.title()

    return spectype_and_format

# Structure mapping the original top level property to a function returning a
# single item dict representing the new property and its value
CHO_TRANSFORMER = {
    "collection"         : lambda d, p: {"collection": getprop(d, p)},
    META + "date"        : date_transform, #DONE
    META + "title"       : title_transform, #DONE
    META + "rights"      : rights_transform, #DONE
    META + "creator"     : creator_transform, #DONE
    META + "subject"     : subject_transform, #DONE
    META + "relation"    : lambda d, p: {"relation": getprop(d, p)},
    META + "language"    : lambda d, p: {"language": getprop(d, p)},
    META + "coverage"    : spatial_transform, #DONE
    META + "publisher"   : publisher_transform, #DONE
    META + "identifier"  : identifier_transform, #DONE
    META + "contributor" : lambda d, p: {"contributor": getprop(d, p)},
    META + "description" : description_transform, #DONE
    META + "resourceType": spectype_and_format_transform #DONE
}

AGGREGATION_TRANSFORMER = {
    "id"                 : lambda d, p: {"id": getprop(d, p),
                                         "@id" : "http://dp.la/api/items/"+ 
                                                 getprop(d, p)},
    "_id"                : lambda d, p: {"_id": getprop(d, p)},
    "provider"           : lambda d, p: {"provider": getprop(d, p)},
    "identifier"         : url_transform,
    "ingestType"         : lambda d, p: {"ingestType": getprop(d, p)},
    "ingestDate"         : lambda d, p: {"ingestDate": getprop(d, p)},
    "originalRecord"     : lambda d, p: {"originalRecord": getprop(d, p)}
}

@simple_service("POST", "http://purl.org/la/dp/oai_untl_to_dpla",
                "oai_untl_to_dpla", "application/ld+json")
def oaiuntltodpla(body, ctype, geoprop=None):
    """
    Convert output of JSON-ified OAI UNTL format into the DPLA JSON-LD format.

    Parameter "geoprop" specifies the property name containing lat/long coords
    """

    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header("content-type","text/plain")
        return "Unable to parse body as JSON"

    global GEOPROP
    GEOPROP = geoprop

    out = {
        "@context": CONTEXT,
        "sourceResource": {}
    }

    # Remove "untl:" prefix from data keys
    data = remove_key_prefix(data, "untl:")

    logger.error("keys: %s" % data.keys())

    # Apply all transformation rules from original document
    for p in CHO_TRANSFORMER:
        if exists(data, p):
            out["sourceResource"].update(CHO_TRANSFORMER[p](data, p))
    for p in AGGREGATION_TRANSFORMER:
        if exists(data, p):
            out.update(AGGREGATION_TRANSFORMER[p](data, p))

    # Strip out keys with None/null values?
    out = dict((k,v) for (k,v) in out.items() if v)

    return json.dumps(out)
