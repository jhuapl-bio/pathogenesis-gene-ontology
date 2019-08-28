#!/usr/bin/env python
#-----------------------------------------------------------
# -*- mode:c++;tab-width:2;indent-tabs-mode:t;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=2 noet:
#
# match_PathGO_to_GO.py
#
# Python file which reads in the PathGO ontology file and queries a Mongo database containing the GO
# ontology to identify similar terms between the two ontologies. 
#
# Authors:  Ron Jacak <ronald.jacak@jhuapl.edu>
# Creation Date:  3 July 2019
#
#------------------------------------------------------------------------------------------
#
from pymongo import MongoClient

import sys
import argparse # for command-line arguments
import logging
import re
import textdistance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_ontology( db, ontology ):
    '''Parse the ontology and return a list of PathGO terms'''

    logger.info( "Parsing ontology for terms." )
    excluded_labels = [ 'definition', 'namespace-id-rule', 'database_cross_reference', 'has_obo_format_version', 
                        'has_obo_namespace', 'has_related_synonym', 'participates_in' ]
    terms = []
    file = open(ontology, "r")
    second_to_last_matched_term_id = None
    last_matched_term_id = None
    for line in file:
        line = line.strip()
        if 'rdfs:label' in line:
            if any(excluded_label in line for excluded_label in excluded_labels): continue
            matches = re.search('>([\w\s\-\/\(\)]*)</rdfs:label>$', line)
            label = matches.group(1)
            term = {}
            term['label'] = label
            term['id'] = last_matched_term_id
            terms.append( term )
            term = None
        elif '<owl:Class' in line:
            # <owl:Class rdf:about="http://purl.obolibrary.org/obo/pathgo/PATHGO_0000002">
            print(line)
            matches = re.search('rdf:about="http:\/\/purl.obolibrary.org\/obo\/pathgo\/(.*)">$', line)
            if matches.group(1) == last_matched_term_id:
                print("ERROR: Found class with no label while parsing ontology.")
                return
            last_matched_term_id = matches.group(1)
        else:
            continue

    logger.info("Found %d terms in passed-in ontology." % len(terms) )
    logger.info( list( terms ) )

    # use the list to set conversion to remove duplicate terms
    return list(terms)

def compare_ontologies( db, pathgo_list ):
    '''One option is to use a Google sentence encoder, as follows:
    #Requirements: Tensorflow>=1.7 tensorflow-hub numpy

    import tensorflow as tf
    import tensorflow_hub as hub
    import numpy as np
    
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
    embed = hub.Module(module_url)
    sentences = ["Python is a good language","Language a good python is"]
    
    similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
    similarity_sentences_encodings = embed(similarity_input_placeholder)
    
    with tf.Session() as session:
      session.run(tf.global_variables_initializer())
      session.run(tf.tables_initializer())
      sentences_embeddings = session.run(similarity_sentences_encodings, feed_dict={similarity_input_placeholder: sentences})
      similarity = np.inner(sentences_embeddings[0], sentences_embeddings[1])
      print("Similarity is %s" % similarity)
    '''
    for go_term in db.go.find( {}, {'_id': 1, 'name': 1 } ):
        #logger.info("compare_ontologies: go term: " + go_term['name'])

        for pathgo_term in pathgo_list:
            #logger.info("compare_ontologies: pathgo term: " + pathgo_term['label'])
       
            if textdistance.ratcliff_obershelp.similarity(go_term['name'], pathgo_term['label']) > 0.75:
               print("%s is similar to %s" % (go_term, pathgo_term))


if __name__ == '__main__':

    # the python argparse module will parse command line options, as well as print a helpful usage prompt if called without parameters
    parser = argparse.ArgumentParser( description='Searches the GO collection in Mongo to find terms similar to the terms in the passed-in ontology.' )
    parser.add_argument('ontology', help="the current version of PathGO from which to pull terms. this should be the owl file of the ontology.") # positional argument
    args = parser.parse_args()

    # establish the DB connection and cursor objects.
    try:
        # connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client.go
    except e:
       sys.stderr.write("[ERROR] %d: %s\n" % (e.args[0], e.args[1]))
       sys.exit(1)

    compare_ontologies( db, process_ontology( db, args.ontology ) )

    # close the connection to MongoDB
    client.close()

