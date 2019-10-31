import gedcom
from gedcom.structures import Line, Header, Submission, Individual, Family,\
    Multimedia, Note, Repository, Source, Submitter
import re

def is_valid_gedcom_line(line):
        """
        Each line should have the following (bracketed items optional):
        level + ' ' + [pointer + ' ' +] tag + [' ' + line_value]
        """
        # Level must start with non-negative int, no leading zeros.
        level_regex = '^(0|[1-9]+[0-9]*) '
        # Pointer optional, if it exists it must be flanked by `@`
        pointer_regex = '(@[^@]+@ |)'
        # Tag must be an alphanumeric string
        tag_regex = '([A-Za-z0-9_]+)'
        # Value optional, consists of anything after a space to end of line
        value_regex = '( [^\n\r]*|)'
        # End of line defined by `\n` or `\r`
        end_of_line_regex = '([\r\n]{1,2})'
        # Complete regex
        gedcom_line_regex = level_regex + pointer_regex + tag_regex + value_regex + end_of_line_regex
        return (re.match(gedcom_line_regex, line) is not None) or (line == '0 '+ gedcom.tags.GEDCOM_TAG_TRAILER) and (len(line) <=255)

def split_text_for_gedcom(full_text, initial_tag, level, max_length):
    gedcom_repr = "%s %s " % (level, initial_tag)
    split_text = list(full_text[0+i:max_length+i] for i in range(0, len(full_text), max_length))
    if len(split_text) == 0:
        return gedcom_repr.strip()
    split_notes = [note.replace("\n", "\n" + str(level+1) +  " " + gedcom.tags.GEDCOM_TAG_CONTINUED + " ") for note in split_text]
    for i, note_list in enumerate(split_notes):
        if i > 0 and not (gedcom.tags.GEDCOM_TAG_CONTINUED in note_list):
            gedcom_repr = gedcom_repr + "\n" + str(level+1) + " "  + gedcom.tags.GEDCOM_TAG_CONCATENATION + " " + "".join(note_list)
        else:
            gedcom_repr += "".join(note_list)
    return gedcom_repr 

class GedcomFormatViolationError(Exception):
    pass

class GedcomFile(object):
    def __init__(self):
        self.__header = None
        self.__submission_record = None
        self.__records = []

    def parse_gedcom(self, file_path):
        gedcom_lines_list = []
        with open(file_path, mode='r', encoding='utf-8-sig') as content_file:
            content = content_file.readlines()
        for index, line in enumerate(content):
            if is_valid_gedcom_line(line):
                gedcom_lines_list.append(Line(line, index))
            else:
                error_message = "Invalid GEDCOM line: " + line
                raise GedcomFormatViolationError(error_message)
        # HEADER record is mandatory and must be the first one
        self.__header = Header()
        parsed_lines = self.__header.parse_gedcom(gedcom_lines_list)
        for line_zero_index in [line for line in gedcom_lines_list[parsed_lines:] if line.level==0]:
            # Submission record is optional
            if line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SUBMISSION:
                record = Submission()
                record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
                self.__submission_record = record
                continue
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_INDIVIDUAL:
                record = Individual()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_FAMILY:
                record = Family()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_OBJECT:
                record = Multimedia()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_NOTE:
                record = Note()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_REPOSITORY:
                record = Repository()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SOURCE:
                record = Source()
            elif line_zero_index.tag == gedcom.tags.GEDCOM_TAG_SUBMITTER:
                record = Submitter()
            elif line_zero_index.is_user_defined_tag():
                continue
            elif line_zero_index.is_last_gedcom_line():
                return
            else:
                return
            record.parse_gedcom(gedcom_lines_list[line_zero_index.gedcom_index:])
            self.__records.append(record)
    
    def get_gedcom_repr(self):
        gedcom_repr = ""
        if self.__header:
            gedcom_repr = self.__header.get_gedcom_repr(0)
        if self.__submission_record:
            gedcom_repr = "%s\n%s" % (gedcom_repr, self.__submission_record.get_gedcom_repr(0))
        for record in self.__records:
            gedcom_repr = "%s\n%s" % (gedcom_repr, record.get_gedcom_repr(0))
        gedcom_repr = "%s\n0 %s" % (gedcom_repr, gedcom.tags.GEDCOM_TAG_TRAILER)
        return gedcom_repr
    
    @property
    def individuals(self):
        return (i for i in self.__records if isinstance(i, Individual))
    
    @property
    def families(self):
        return (i for i in self.__records if isinstance(i, Family))
