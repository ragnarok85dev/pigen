import unittest
import os.path
from gedcom.structures import Individual, NoteStructure, MultimediaLink,\
    SourceCitation, PersonalNameStructure, ChangeDate, AddressStructure, Line

def file_to_string(file_path):
    with open(file_path, 'r') as file:
        outstring = file.read()
    return outstring

def file_to_gedcom_lines(file_path):
    gedcom_lines_list = []
    with open(file_path, mode='r', encoding='utf-8-sig') as content_file:
        content = content_file.readlines()
    for line in content:
        gedcom_lines_list.append(Line(line))
    return gedcom_lines_list


# class TestIndividual(unittest.TestCase):
#     maxDiff = None
#     def testIndividual(self):
#         starting_gedcom_level = 0
#         filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/individual_record_chunk_1")
#         record = Individual(file_to_gedcom_lines(filepath))
#         read_file = file_to_string(filepath)
#         self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level))

class TestAddressStructure(unittest.TestCase):
    COMPONENT_NAME = "AddressStructure"
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/address_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = AddressStructure()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testAddressStructureSimple1(self):
        for i in range(1, 6):
            self.simpleCall(i)

class TestChangeDate(unittest.TestCase):
    COMPONENT_NAME = "ChangeDate"

    def simpleCall(self, index, expected_outcome):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/change_date_structure_chunk_" + index)
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = ChangeDate()
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
        record = ChangeDate()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        expected_outcome = """2 CHAN
3 DATE 18-giu-2019
4 TIME 00:01
3 NOTE this is a line
4 CONT And this is another line is ending here."""
        self.assertEqual(expected_outcome, record.get_gedcom_repr(starting_gedcom_level), error_message)


class TestLine(unittest.TestCase):
    def testFullLine(self):
        gedcom_line = "0 @pointer@ TAG This is the value"
        line = Line(gedcom_line)
        reconstructed_line = "%s %s %s %s" % (line.level, line.pointer, line.tag, line.value) 
        self.assertEqual(gedcom_line, reconstructed_line)
        self.assertEqual(0, line.level)
        self.assertEqual("@pointer@", line.pointer)
        self.assertEqual("TAG", line.tag)
        self.assertEqual("This is the value", line.value)

    def testOnlyTag(self):
        gedcom_line = "0 HEAD"
        line = Line(gedcom_line)
        reconstructed_line = "%s %s" % (line.level, line.tag) 
        self.assertEqual(gedcom_line, reconstructed_line)
        self.assertEqual(0, line.level)
        self.assertEqual("HEAD", line.tag)
        self.assertEqual("", line.value)
        self.assertEqual("", line.pointer)

    def testNoPointer(self):
        gedcom_line = "0 NOTE This is a note"
        line = Line(gedcom_line)
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
        parsed_substructure = MultimediaLink()
        parsed_substructure.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, parsed_substructure.get_gedcom_repr(starting_gedcom_level), error_message)

    def testMultimediaLink(self):
        for i in range(1, 3):
            self.simpleCall(i)

class TestPersonalNameStructure(unittest.TestCase):
    COMPONENT_NAME = "PersonalNameStructure"
    maxDiff = None
    
    def simpleCall(self, index):
        starting_gedcom_level = 2
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/personal_name_structure_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        parsed_substructure = PersonalNameStructure()
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
        parsed_note = NoteStructure()
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

class TestSourceCitation(unittest.TestCase):
    COMPONENT_NAME = "SourceCitation"
    def simpleCall(self, index):
        starting_gedcom_level = 3
        filepath = os.path.join(os.path.abspath(__file__), "../gedcom_files/source_citation_chunk_" + str(index))
        error_message = "\n" + self.COMPONENT_NAME + " unit test error parsing " + filepath
        record = SourceCitation()
        record.parse_gedcom(file_to_gedcom_lines(filepath))
        read_file = file_to_string(filepath)
        self.assertEqual(read_file, record.get_gedcom_repr(starting_gedcom_level), error_message)

    def testSourceCitation(self):
        for i in range(1, 6):
            self.simpleCall(i)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLine']
    unittest.main()