import unittest
from gedcom.line import Line


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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLine']
    unittest.main()