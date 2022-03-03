import unittest
import networkx

from propagate_PathGO_annotations import get_parents, process_pathgo_ontology, propagate_annotations

class TestGetTerms(unittest.TestCase):
 
    @classmethod
    def setUpClass(cls):
        cls.graph = process_pathgo_ontology( "./pathgo.obo" )

    def test_get_parents_easy_names(self):
        correct_terms = [ 'direct mechanism of pathogenicity', 'mechanism of pathogenicity' ]
        self.assertEqual( get_parents( self.graph, 'PATHGO:0000164', ids=False ), correct_terms )
 
    def test_get_parents_hard_names(self):
        correct_terms = [ "mediates activation of small GTPase in another organism", "modulates small GTPase activity in another organism",
        "modulates G-protein signaling pathways in another organism", "disrupts cellular signaling in another organism",
        "direct mechanism of pathogenicity", "mechanism of pathogenicity" ]
        correct_terms.sort()
        self.assertEqual( get_parents( self.graph, "PATHGO:0000255", ids=False ), correct_terms )

    def test_get_parents_root_names(self):
        correct_terms = [ ]
        self.assertEqual( get_parents( self.graph, "PATHGO:0000114", ids=False ), correct_terms )

    def test_get_parents_indirect_branch_names(self):
        correct_terms = [ "promotes survival in host", "mediates iron acquisition", "mediates nutrient acquisition",
        "indirect mechanism of pathogenicity", "mechanism of pathogenicity" ]
        correct_terms.sort()
        self.assertEqual( get_parents( self.graph, "PATHGO:0000124", ids=False ), correct_terms )

    def test_get_parents_easy(self):
        correct_terms = [ "PATHGO:0000333", "PATHGO:0000114" ]
        self.assertEqual( get_parents( self.graph, "PATHGO:0000164" ), correct_terms )

    def test_get_parents_hard(self):
        correct_terms = [ "PATHGO:0000333", "PATHGO:0000165", "PATHGO:0000114", "PATHGO:0000356", "PATHGO:0000175", "PATHGO:0000328" ]
        self.assertEqual( get_parents( self.graph, "PATHGO:0000255" ), correct_terms )

    def test_get_parents_root(self):
        correct_terms = [ ]
        self.assertEqual( get_parents( self.graph, "PATHGO:0000114" ), correct_terms )

    def test_propagate_annotations_easy(self):
        correct_lines = [
            'B8XH01,PATHGO:0000164,disrupts cellular metabolism in another organism,PMID: 15680238',
            'B8XH01,PATHGO:0000333,direct mechanism of pathogenicity,PMID: 15680238',
            'B8XH01,PATHGO:0000114,mechanism of pathogenicity,PMID: 15680238'
        ]
        self.assertEqual( propagate_annotations( self.graph, "./annotations_test_easy.txt" ), correct_lines )
        
    def test_propagate_annotations_hard(self):
        correct_lines = [
            'P01501,PATHGO:0000033,mediates pore formation in another organism,PMID: 4057243; PubMed:6830776',
            'P01501,PATHGO:0000333,direct mechanism of pathogenicity,PMID: 4057243; PubMed:6830776, PMID: 26983715, PMID6830776; PMID: 30885804',
            'P01501,PATHGO:0000166,disrupts cellular structure in another organism,PMID: 4057243; PubMed:6830776, PMID6830776; PMID: 30885804',
            'P01501,PATHGO:0000114,mechanism of pathogenicity,PMID: 4057243; PubMed:6830776, PMID: 26983715, PMID6830776; PMID: 30885804',
            'P01501,PATHGO:0000029,mediates membrane damage of another organism,PMID: 4057243; PubMed:6830776, PMID6830776; PMID: 30885804',
            'P01501,PATHGO:0000176,modulates receptor activity in another organism,PMID: 26983715',
            'P01501,PATHGO:0000165,disrupts cellular signaling in another organism,PMID: 26983715'
        ]
        self.assertEqual( propagate_annotations( self.graph, "./annotations_test_hard.txt" ), correct_lines )

if __name__ == '__main__':
    unittest.main()
