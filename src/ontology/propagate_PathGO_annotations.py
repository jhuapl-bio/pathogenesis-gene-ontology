#!/usr/bin/env python
#-----------------------------------------------------------
# -*- mode:c++;tab-width:2;indent-tabs-mode:t;show-trailing-whitespace:t;rm-trailing-spaces:t -*-
# vi: set ts=2 noet:
#
# propagate_PathGO_annotations.py
#
# Takes a file of PathGO term annotations on sequences and a file with the PathGO ontology and propagates all the annotations
#
# Authors:  Ron Jacak <ronald.jacak@jhuapl.edu>
# Creation Date:  24 Feb 2022
#
#------------------------------------------------------------------------------------------
#
import sys
import argparse # for command-line arguments
import logging
import obonet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_pathgo_ontology( ontology ):
    '''Parse the ontology and return a list of PathGO terms'''

    logger.info( "Parsing ontology for terms." )

    excluded_labels = [ 'definition', 'namespace-id-rule', 'database_cross_reference', 'has_obo_format_version',
                        'has_obo_namespace', 'has_related_synonym', 'participates_in' ]
    terms = []
    file = open(ontology, "r")

    graph = obonet.read_obo(ontology)

    for node in graph:
       
       if node == "None": continue

       path_go_term = graph.nodes[node]
       if path_go_term == {}: continue # this can occur if you delete half the ontology, for example. guess the obonet parser creates nodes for terms that aren't defined in the file.

       #print("process_pathgo_ontology(): path_go_term: ")
       #print(path_go_term)
       
       term = {}
       term['name'] = path_go_term['name']
       term['label'] = node
       
       term['definition'] = ""
       if 'def' in path_go_term:
          term['definition'] = path_go_term['def']

       editorialNote = None
       comment = None

       # {'name': 'cell surface binding factor', 'is_a': ['PATHGO:0000120'],
       # 'property_value': ['editorialNote "sialyl Lewis x binding protein is an example\\n\\nbuild out subclasses" xsd:string', 'IAO:0000115 "A gene product that mediates adhesion by enabling binding to cell surface receptors or components." xsd:string']}
       
       if 'property_value' in path_go_term:
          # property_value is actually a list that we need to parse
          for value in path_go_term['property_value']:
             if value.startswith( "editorialNote" ):
                editorialNote =  value.replace("editorialNote ", "").replace(" xsd:string", "")
                #print(editorialNote)

       term['is_a'] = ""
       if term['name'] != "mechanism of pathogenicity":
          term['is_a'] = path_go_term['is_a'][0] # for some reason these are stored as an array in the obo.  multiple inheritance???

       if term['name'] != "mechanism of pathogenicity" and term['is_a'] == "":
          print("Found non-root term without is_a value: " + term['label'] )
          sys.exit(1)

       if 'comment' in path_go_term:
          comment = path_go_term['comment']

       # looks like we've used both editorialComment and comment in the ontology.  sort of which one to use for the term here.
       term['comments'] = ""
       if editorialNote and comment:
          print("Term has both editorialNote and comment.  Is this intentional?")
          term['comments'] = editorialNote
          #sys.exit()
       if editorialNote:
          term['comments'] = editorialNote
       if comment:
          term['comments'] = comment
       
       term['xref'] = ""
       if 'xref' in path_go_term:
          term['xref'] = str(','.join( path_go_term['xref'] ))

       terms.append( [ term['name'], term['label'], term['is_a'], term['definition'], term['xref'], term['comments'] ] )
       term = None


    logger.info("Found %d terms in passed-in ontology." % len(terms) )
    for term in terms:
       logger.info( term )

    # use the list to set conversion to remove duplicate terms
    return terms


def read_annotations( annotations_file ):
    '''Reads in the annotations into a list and returns that list.'''

    return None


if __name__ == '__main__':

    # the python argparse module will parse command line options, as well as print a helpful usage prompt if called without parameters
    parser = argparse.ArgumentParser( description='Takes a file of PathGO term annotations on sequences and a file with the PathGO ontology and propagates all the annotations.' )
    parser.add_argument('ontology', help="an obo file representing the version of PathGO to use for propagation.") # positional argument
    parser.add_argument('annotations', help="file containing the annotations to propagate.") # positional argument
    args = parser.parse_args()

    process_pathgo_ontology( args.ontology )

    read_annotations( args.annotations )


    logger.info("Done.")

