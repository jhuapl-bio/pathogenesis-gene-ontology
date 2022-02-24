import unittest

from propagate_PathGO_annotations import what?

class TestGetTerms(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_process_one_term(self):
        correct_terms = [ "GO:0048308", "GO:0048311", "GO:0006996", "GO:0007005", "GO:0016043", "GO:0009987", "GO:0008150", "GO:0071840", "GO:0051646", "GO:0051640", "GO:0051641", "GO:0051179" ]
        correct_terms.sort()
        self.assertEqual( process_GO_terms( db, ["GO:0000001"]), correct_terms )
 
    def test_process_several_terms(self):
        correct_terms = [ "GO:0005488", "GO:0003674", "GO:0036094", "GO:1901265", "GO:0097159", "GO:1901363", "GO:0005488", "GO:0003674",
                          "GO:0030597", "GO:0140102", "GO:0140098", "GO:0016799", "GO:0016798", "GO:0016787", "GO:0003824", "GO:0003674",
                          "GO:0044419", "GO:0051704", "GO:0008150", "GO:0006950", "GO:0050896",
                          "GO:0044364", "GO:0001906", "GO:0035821", "GO:0044419", "GO:0006417",
                          "GO:0010629", "GO:0010468", "GO:0010605", "GO:0060255", "GO:0009892", "GO:0019222",
                          "GO:0048519", "GO:0050789", "GO:0065007", "GO:0032269", "GO:2000113", "GO:0034249", "GO:0006417", "GO:0008150", "GO:0009889", 
                          "GO:0009890", "GO:0009892", "GO:0010468", "GO:0010556", "GO:0010558", "GO:0010605", 
                          "GO:0010608", "GO:0010629", "GO:0019222", "GO:0031323", "GO:0031324", "GO:0031326", 
                          "GO:0031327", "GO:0032268", "GO:0032269", "GO:0034248", "GO:0034249", "GO:0048519", 
                          "GO:0048523", "GO:0050789", "GO:0050794", "GO:0051171", "GO:0051172", "GO:0051246", 
                          "GO:0051248", "GO:0060255", "GO:0065007", "GO:0080090", "GO:2000112", "GO:2000113" ]
        unique_correct_terms = list( set( correct_terms ) )
        unique_correct_terms.sort()
        self.assertEqual( process_GO_terms( db, ["GO:0030246", "GO:0000166", "GO:0030598", "GO:0090729", "GO:0006952", "GO:0031640", "GO:0017148"] ), unique_correct_terms )

    def test_process_multi_inheritance(self):
        correct_terms = [ "GO:0009372", "GO:0048874", "GO:0044764", "GO:0048872", "GO:0051704", "GO:0008150", "GO:0009987", "GO:0042592", "GO:0065008", "GO:0065007", "GO:0044419" ]
        correct_terms.sort()
        self.assertEqual( process_GO_terms( db, ["GO:0052097"]), correct_terms )


if __name__ == '__main__':
    unittest.main()

