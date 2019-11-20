import unittest
import os.path
import gedcom.structures
from gedcom.gedcom_file import GedcomFile, GedcomLine

def file_to_string(file_path):
    with open(file_path, 'r') as file:
        outstring = file.read()
    return outstring

def file_to_gedcom_lines(file_path):
    gedcom_lines_list = []
    with open(file_path, mode='r', encoding='utf-8-sig') as content_file:
        content = content_file.readlines()
    for line in content:
        gedcom_lines_list.append(GedcomLine(line))
    return gedcom_lines_list

class TestHeader(unittest.TestCase):
    COMPONENT_NAME = "Header"
    maxDiff = None

    def simpleCall(self, index):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/header_test_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        header = gedcom.structures.Header()
        header.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, header.get_gedcom_repr(starting_gedcom_level), error_message)

    def testHeader1(self):
        self.simpleCall(1)

    def testHeader2(self):
        input_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/header_test_2")
        compare_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/header_test_2_compare")
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + input_filepath
        header = gedcom.structures.Header()
        header.parse_gedcom(file_to_gedcom_lines(input_filepath))
        compare_file = file_to_string(compare_filepath)
        self.assertEqual(compare_file, header.get_gedcom_repr(0), error_message)

class TestIndividual(unittest.TestCase):
    maxDiff = None
    COMPONENT_NAME = "Individual"
     
    def simpleCall(self, index):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_record_chunk_" + str(index))
        record = gedcom.structures.Individual()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level))
 
    def testIndividualRecord1(self):
        self.simpleCall(1)
 
    def testIndividualRecord2(self):
        self.simpleCall(2)
 
    def testIndividualRecord3(self):
        input_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_record_chunk_3")
        compare_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_record_chunk_3_compare")
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + input_filepath
        record = gedcom.structures.Individual()
        record.parse_gedcom(file_to_gedcom_lines(input_filepath))
        compare_file = file_to_string(compare_filepath)        
        file = open("C:\\Users\\gricca4\\LocalData\\pigen\\temp.txt","w")
        file.write(record.get_gedcom_repr(0))
        file.close()
        self.assertEqual(compare_file, record.get_gedcom_repr(0), error_message)

class TestAddressStructure(unittest.TestCase):
    COMPONENT_NAME = "AddressStructure"
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/address_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.AddressStructure()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testAddressStructure(self):
        for i in range(1, 6):
            self.simpleCall(i)

class TestChildToFamilyLink(unittest.TestCase):
    COMPONENT_NAME = "ChildToFamilyLink"
    maxDiff = None
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/child_to_family_link_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = gedcom.structures.ChildToFamilyLink()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testChildToFamilyLink(self):
        for i in range(1, 4):
            self.simpleCall(i)

class TestChangeDate(unittest.TestCase):
    COMPONENT_NAME = "ChangeDate"

    def simpleCall(self, index, expected_outcome):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/change_date_structure_chunk_" + index)
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.ChangeDate()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        self.assertEqual(expected_outcome, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testChangeDateSimple1(self):
        self.simpleCall("1", "2 CHAN\n3 DATE 18-giu-2019")

    def testChangeDateSimple2(self):
        self.simpleCall("2", "2 CHAN\n3 DATE 18-giu-2019\n4 TIME 00:01")
    
    def testChangeDate3(self):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/change_date_structure_chunk_3")
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.ChangeDate()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        expected_outcome = """2 CHAN
3 DATE 18-giu-2019
4 TIME 00:01
3 NOTE this is a line
4 CONT And this is another line is ending here."""
        self.assertEqual(expected_outcome, record.get_gedcom_repr(starting_gedcom_level), error_message)

class TestEventDetail(unittest.TestCase):
    COMPONENT_NAME = "EventDetail"
    maxDiff = None
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/event_detail_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.EventDetail()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testEventDetail1(self):
        for i in range(1,3):
            self.simpleCall(i)

class TestFamilyEventDetail(unittest.TestCase):
    COMPONENT_NAME = "FamilyEventDetail"
    maxDiff = None

    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/family_event_detail_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = gedcom.structures.FamilyEventDetail()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testFamilyEventDetail(self):
        for i in range(1,3):
            self.simpleCall(i)

class TestFamilyEventStructure(unittest.TestCase):
    COMPONENT_NAME = "FamilyEventStructure"
    maxDiff = None
    
    def simpleCall(self, index):
        starting_gedcom_level = 1
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/family_event_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = gedcom.structures.FamilyEventStructure()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testFamilyEventStructure(self):
        for i in range(1,4):
            self.simpleCall(i)

class TestFamilyRecord(unittest.TestCase):
    COMPONENT_NAME = "FamilyRecord"
    maxDiff = None

    def simpleCall(self, index):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/family_record_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.Family()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testFamilyRecord(self):
        for i in range(1,3):
            self.simpleCall(i)

class TestIndividualEventDetail(unittest.TestCase):
    COMPONENT_NAME = "IndividualEventDetail"
    maxDiff = None
     
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_event_detail_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.IndividualEventDetail()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)
 
    def testIndividualEventDetail1(self):
        for i in range(1,2):
            self.simpleCall(i)

class TestIndividualAttributeStructure(unittest.TestCase):
    COMPONENT_NAME = "IndividualAttributeStructure"
    maxDiff = None
     
    def simpleCall(self, index):
        starting_gedcom_level = 1
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_attribute_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.IndividualAttributeStructure()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)
 
    def testIndividualAttributeStructure(self):
        for i in range(1,4):
            self.simpleCall(i)

class TestIndividualEventStructure(unittest.TestCase):
    COMPONENT_NAME = "IndividualEventStructure"
    maxDiff = None
     
    def simpleCall(self, index):
        starting_gedcom_level = 1
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_event_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.IndividualEventStructure()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)
 
    def testIndividualEventStructure(self):
        for i in range(1,4):
            self.simpleCall(i)

class TestLine(unittest.TestCase):
    def testFullLine(self):
        gedcom_line = "0 @pointer@ TAG This is the value"
        line = GedcomLine(gedcom_line)
        reconstructed_line = "%s %s %s %s" % (line.level, line.pointer, line.tag, line.value) 
        self.assertEqual(gedcom_line, reconstructed_line)
        self.assertEqual(0, line.level)
        self.assertEqual("@pointer@", line.pointer)
        self.assertEqual("TAG", line.tag)
        self.assertEqual("This is the value", line.value)

    def testOnlyTag(self):
        gedcom_line = "0 HEAD"
        line = GedcomLine(gedcom_line)
        reconstructed_line = "%s %s" % (line.level, line.tag) 
        self.assertEqual(gedcom_line, reconstructed_line)
        self.assertEqual(0, line.level)
        self.assertEqual("HEAD", line.tag)
        self.assertEqual("", line.value)
        self.assertEqual("", line.pointer)

    def testNoPointer(self):
        gedcom_line = "0 NOTE This is a note"
        line = GedcomLine(gedcom_line)
        reconstructed_line = "%s %s %s" % (line.level, line.tag, line.value) 
        self.assertEqual(gedcom_line, reconstructed_line)
        self.assertEqual(0, line.level)
        self.assertEqual("NOTE", line.tag)
        self.assertEqual("This is a note", line.value)
        self.assertEqual("", line.pointer)

class TestMultimediaLink(unittest.TestCase):
    COMPONENT_NAME = "MultimediaLink"
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/multimedia_link_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = gedcom.structures.MultimediaLink()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testMultimediaLink(self):
        for i in range(1, 3):
            self.simpleCall(i)

class TestNoteRecord(unittest.TestCase):
    COMPONENT_NAME = "NoteRecord"
    maxDiff = None

    def testNoteRecord1(self):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/note_record_chunk_1")
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.Note()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

class TestPersonalNameStructure(unittest.TestCase):
    COMPONENT_NAME = "PersonalNameStructure"
    maxDiff = None
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/personal_name_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = gedcom.structures.PersonalNameStructure()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testPersonalNameStructure(self):
        for i in range(1, 5):
            self.simpleCall(i)

class TestNoteStructure(unittest.TestCase):
    COMPONENT_NAME = "NoteStructure"

    def simpleCall(self, index, expected_outcome):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/note_structure_chunk_" + index)
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_note = gedcom.structures.NoteStructure()
        parsed_note.parse_gedcom(file_to_gedcom_lines(filepath))
        self.assertEqual(expected_outcome, parsed_note.get_gedcom_repr(starting_gedcom_level), error_message)

    def testNoteStructureSimple1(self):
        self.simpleCall("1", "2 NOTE @REF1@")

    def testNoteStructureSimple2(self):
        self.simpleCall("2", "2 NOTE")
        
    def testNoteStructureSimple3(self):
        self.simpleCall("3", "2 NOTE this is a line")
        
    def testNoteStructureSimple4(self):
        self.simpleCall("4", "2 NOTE this is a lineand this is anotherand this is the last one")
        
    def testNoteStructureSimple5(self):
        self.simpleCall("5", "2 NOTE this is a line\n3 CONT And this is another\n3 CONT And this is the last one")

class TestRepositoryRecord(unittest.TestCase):
    COMPONENT_NAME = "RepositoryRecord"
    maxDiff = None

    def testRepositoryRecord(self):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/repository_record_chunk_1")
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.Repository()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

class TestSourceCitation(unittest.TestCase):
    COMPONENT_NAME = "SourceCitation"
    def simpleCall(self, index):
        starting_gedcom_level = 3
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/source_citation_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.SourceCitation()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testSourceCitation(self):
        for i in range(1, 6):
            self.simpleCall(i)

class TestSourceRecord(unittest.TestCase):
    COMPONENT_NAME = "SourceRecord"
    maxDiff = None

    def simpleCall(self, index):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/source_record_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.Source()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testSourceRecord(self):
        for i in range(1, 3):
            self.simpleCall(i)

class TestSpouseToFamilyLink(unittest.TestCase):
    COMPONENT_NAME = "SpouseToFamilyLink"
    maxDiff = None

    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/spouse_to_family_link_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = gedcom.structures.SpouseToFamilyLink()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testSpouseToFamilyLinkSimple1(self):
        self.simpleCall(1)

    def testSpouseToFamilyLinkSimple2(self):
        self.simpleCall(2)

class TestSubmissionRecord(unittest.TestCase):
    COMPONENT_NAME = "SubmissionRecord"
    maxDiff = None

    def simpleCall(self, index):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/submission_record_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.Submission()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testSubmissionRecord(self):
        for i in range(1, 3):
            self.simpleCall(i)

class TestSubmitterRecord(unittest.TestCase):
    COMPONENT_NAME = "SubmitterRecord"
    maxDiff = None

    def testSubmitterRecord(self):
        starting_gedcom_level = 0
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/submitter_record_chunk_1")
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = gedcom.structures.Submitter()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

class TestGedcom(unittest.TestCase):
    maxDiff = None

    def simpleCall(self, file_name):
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/" + file_name)
        error_message = "\n" + "GEDCOM file unit test error parsing " + filepath
        gedcom = GedcomFile()
        gedcom.parse_gedcom(filepath)
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, gedcom.get_gedcom_repr(), error_message)

    def testGedcomSimple(self):
        self.simpleCall("simple.ged")

    def testGedcomComplex(self):
        input_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/allged.ged")
        compare_filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/allged_compare.ged")
        error_message = "\n" + "GEDCOM file unit test error parsing " + input_filepath
        gedcom = GedcomFile()
        gedcom.parse_gedcom(input_filepath)
        compare_file = file_to_string(compare_filepath)
        self.assertEqual(compare_file, gedcom.get_gedcom_repr(), error_message)

if __name__ == "__main__":

    unittest.main()