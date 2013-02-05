"""
Akara module for extracting document source from dplaSourceRecord;
Assumes that original version of document is stored at dplaSourceRecord key in a json tree.
"""

__author__ = 'alexey'

import re

from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json

HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_TYPE_JSON = 'application/json'
HTTP_TYPE_TEXT = 'text/plain'
HTTP_HEADER_TYPE = 'Content-Type'

@simple_service('POST', 'http://purl.org/la/dp/artstor_select_isshownat', 'artstor_select_isshownat', HTTP_TYPE_JSON)
def artstor_select_source(body, ctype):

    LOG_JSON_ON_ERROR = True
    def log_json():
        if LOG_JSON_ON_ERROR:
            logger.debug(body)

    try:
        assert ctype == HTTP_TYPE_JSON, "%s is not %s" % (HTTP_HEADER_TYPE, HTTP_TYPE_JSON)
        data = json.loads(body)
    except Exception as e:
        error_text = "Bad JSON: %s: %s" % (e.__class__.__name__, str(e))
        logger.exception(error_text)
        response.code = HTTP_INTERNAL_SERVER_ERROR
        response.add_header(HTTP_HEADER_TYPE, HTTP_TYPE_TEXT)
        return error_text

    original_document_key = u"dplaSourceRecord"
    original_sources_key = u"handle"
    artstor_source_prefix = "Image View"
    source_key = u"source"

    if original_document_key not in data:
        logger.error("There is no '%s' key in JSON for doc [%s].", original_document_key, data[u'id'])
        log_json()
        return body

    if original_sources_key not in data[original_document_key]:
        logger.error("There is no '%s/%s' key in JSON for doc [%s].", original_document_key, original_sources_key, data[u'id'])
        log_json()
        return body

    source = None
    http_re = re.compile("https?://.*$", re.I)
    for s in data[original_document_key][original_sources_key]:
        if s.startswith(artstor_source_prefix):
            match = re.search(http_re, s)
            if match:
                source = match.group(0)
                break

    if not source:
        logger.error("Can't find url with '%s' prefix in [%s] for fetching document source for Artstor.", artstor_source_prefix, data[original_document_key][original_sources_key])
        log_json()
        return body

    data[source_key] = source
    return json.dumps(data)

