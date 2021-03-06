#!/usr/bin/env python
"""
Script to save data from JSON files to the CouchDB database

Usage:
    $ python save_records.py ingestion_document_id
"""
import os
import sys
import shutil
import argparse
import ConfigParser
from akara import logger
from datetime import datetime
from amara.thirdparty import json
from dplaingestion.couch import Couch
from dplaingestion.selector import getprop
from dplaingestion.utilities import make_tarfile

def define_arguments():
    """Defines command line arguments for the current script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("ingestion_document_id", 
                        help="The ID of the ingestion document")

    return parser

def main(argv):
    parser = define_arguments()
    args = parser.parse_args(argv[1:])

    config = ConfigParser.ConfigParser()
    config.readfp(open("akara.ini"))
    batch_size = int(config.get("CouchDb", "IterviewBatch"))

    couch = Couch()
    ingestion_doc = couch.dashboard_db[args.ingestion_document_id]
    if getprop(ingestion_doc, "enrich_process/status") != "complete":
        print "Cannot save, enrich process did not complete"
        return -1

    # Update ingestion document
    kwargs = {
        "save_process/status": "running",
        "save_process/start_time": datetime.now().isoformat()
    }
    try:
        couch.update_ingestion_doc(ingestion_doc, **kwargs)
    except:
        print "Error updating ingestion document " + ingestion_doc["_id"]
        return -1

    # Back up provider data
    resp = couch._back_up_data(ingestion_doc)

    if resp == -1:
        # Fatal error, do not continue with save process
        kwargs = {
            "save_process/status": "error",
            "save_process/end_time": datetime.now().isoformat(),
            "save_process/error": "Error backing up DPLA records"
        }
        couch.update_ingestion_doc(ingestion_doc, **kwargs)
        return resp

    error_msg = None
    enrich_dir = getprop(ingestion_doc, "enrich_process/data_dir")
    total_saved_documents = 0
    docs = {}
    for file in os.listdir(enrich_dir):
        filename = os.path.join(enrich_dir, file)
        with open(filename, "r") as f:
            try:
                docs.update(json.loads(f.read()))
            except:
                error_msg = "Error loading " + filename
                break

        # Save only when the number of docs exceeds the batch size
        if len(docs) > batch_size:
            resp, error_msg = couch.process_and_post_to_dpla(docs,
                                                             ingestion_doc)
            if resp == -1:
                break
            else:
                total_saved_documents += len(docs)
                print "Saved %s documents" % total_saved_documents
                docs = {}
    # Last save
    if docs:
        resp, error_msg = couch.process_and_post_to_dpla(docs,
                                                         ingestion_doc)
        if resp != -1:
            total_saved_documents += len(docs)
            print "Saved %s documents" % total_saved_documents

    logger.info("Total documents saved: %s (*includes duplicate collections)" %
                total_saved_documents)

    if error_msg:
        status = "error"
    else:
        status = "complete"
    kwargs = {
        "save_process/status": status,
        "save_process/error": error_msg,
        "save_process/end_time": datetime.now().isoformat()
    }
    try:
        couch.update_ingestion_doc(ingestion_doc, **kwargs)
    except:
        print "Error updating ingestion document " + ingestion_doc["_id"]
        return -1

    # Compress enrich dir, then delete
    make_tarfile(enrich_dir)
    shutil.rmtree(enrich_dir)

    return 0 if status == "complete" else -1

if __name__ == '__main__':
    main(sys.argv)
