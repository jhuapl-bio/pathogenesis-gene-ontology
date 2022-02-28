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
import networkx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_parents( graph, term, ids=True ):
    '''Takes in the graph and the term and returns a list of the parents of the passed-in term'''
    
    # use the networkx descendants function (which ironically gets the ancestors) to get all the parents
    #print("Parents: " + term + " -> ", end='')
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    parents = sorted( id_to_name[superterm] for superterm in networkx.descendants(graph, term ) )
    if not ids:
       return parents
    else:
       name_to_id = { data['name']: id_ for id_, data in graph.nodes(data=True) if 'name' in data }
       parents_ids = []
       for parent in parents:
          parents_ids.append( name_to_id[ parent ] )

    #print(parents)
    return parents_ids


def process_pathgo_ontology( ontology ):
    '''Parse the ontology and return a list of PathGO terms'''

    logger.info( "Parsing ontology file " + ontology + " for terms." )
    file = open(ontology, "r")
    graph = obonet.read_obo(ontology)
    file.close()

    return graph


def propagate_annotations( graph, annotations_file ):
    '''Reads in the annotations into a list and returns that list.'''

    annotations_data_structure = {}
    with open( annotations_file ) as file:
        lines = [line.rstrip() for line in file]

    # remove header line
    lines.pop(0)

    for line in lines:
        logger.info( line )

        #Uniprot_id,PathGO_id,PathGO_name
        #Q14U76,PATHGO:0000085,mediates immune evasion and subversion in another organism

        uniprot_id, pathgo_id, pathgo_name, reference = line.split(',',maxsplit=3)

        id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
        # a little sanity check to make sure the ontology file and the annotations file are in sync
        if pathgo_name != id_to_name[ pathgo_id ]:
            print( "Node name not equal to what was found in file." )

        # need to create a data structure that will hold the propagated annotations
        # let's create a dictionary of dictionaries keyed on uniprot id and then on pathgo_id that points to a reference value
        # that way if we encounter a leaf node term annotation that propagates all the way up to root, followed by another line that has a non-leaf node term, but some other reference
        # we can append that reference to existing reference
        # 1ABC, PATHGO:101, Foo 2020
        # 1ABC, PATHGO:102, Bar 2018 (102 is a child of 101)
       
        # then [1ABC][PATHGO:101] would get "Foo 2020, Bar 2018" saved, but
        # [1ABC][PATHGO:102] would still just have "Bar 2018"
       
        if uniprot_id not in annotations_data_structure:
            annotations_data_structure[ uniprot_id ] = {}
    
        if pathgo_id not in annotations_data_structure[ uniprot_id ]:
            annotations_data_structure[ uniprot_id ][ pathgo_id ] = reference
        else:
            annotations_data_structure[ uniprot_id ][ pathgo_id ] += ", " + reference

        parents = get_parents( graph, pathgo_id )
        for parent in parents:
            if parent not in annotations_data_structure[ uniprot_id ]:
                annotations_data_structure[ uniprot_id ][ parent ] = reference
            else:
                annotations_data_structure[ uniprot_id ][ parent ] += ", " + reference

    # iterate over the data structure and write out all the lines
    propagated_lines = []
    for id in annotations_data_structure:
        for term_id in annotations_data_structure[ id ]:
            propagated_lines.append( id + "," + term_id + "," + id_to_name[ term_id ] + "," + annotations_data_structure[ id][term_id] )

    return propagated_lines
    

def write_propagated_annotations( annotations_file, lines ):

    output_name = annotations_file.split(".")[0] + ".propagated." + annotations_file.split(".")[1] + "." + annotations_file.split(".")[2]
    output_file = open( output_name, "w" )

    for line in lines:
        output_file.write( line + "\n" )

    output_file.close()


if __name__ == '__main__':

    # the python argparse module will parse command line options, as well as print a helpful usage prompt if called without parameters
    parser = argparse.ArgumentParser( description='Takes a file of PathGO term annotations on sequences and a file with the PathGO ontology and propagates all the annotations.' )
    parser.add_argument('ontology', help="an obo file representing the version of PathGO to use for propagation.") # positional argument
    parser.add_argument('annotations', help="file containing the annotations to propagate.") # positional argument
    args = parser.parse_args()

    graph = process_pathgo_ontology( args.ontology )
    propagated_lines = propagate_annotations( graph, args.annotations )
    write_propagated_annotations( args.annotations, propagated_lines )
    
    logger.info("Done.")

