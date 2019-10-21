import re
import gedcom

gedcom_line_format = re.compile("^(?P<level>[0-9]+) ((?P<id>@[-a-zA-Z0-9]+@) )?(?P<tag>[_A-Z0-9]+)( (?P<value>.*))?$")

class Line(object):
    """
    Each GEDCOM line has the following syntax:
    gedcom_line := level + ' ' + [pointer + ' ' +] tag + [' ' + line_value]
    where:
        level is an integer number from 0 to 99, without leading zero
        optional_pointer is an optional pointer followed by delim, where point has the form @alphanum@
        tag is an alphanumeric string
        optional_line_value is the value associated to the tag
        terminator is carriage return and/or line feed
        implicit delimiter of elements is the space character
    """
    
    def __init__(self, line_content, index=0):
        self.__content = line_content
        self.__gedcom_index = index
        match = re.match(gedcom_line_format, line_content)
        if match:
            self.__level = int(match[1])
            if match[2]:
                self.__pointer = match[2].strip()
            else:
                self.__pointer = ""
            self.__tag = match[4].strip()
            if match[5]:
                self.__value = match[5].strip()
            else:
                self.__value = ""

    def is_last_gedcom_line(self):
        return self.__content == '0 '+ gedcom.tags.GEDCOM_TAG_TRAILER
    
    def is_user_defined_tag(self):
        return self.__tag[0:1] == '_'

    def get_content(self):
        return self.__content

    def get_gedcom_index(self):
        return self.__gedcom_index

    def get_level(self):
        return self.__level

    def get_pointer(self):
        return self.__pointer

    def get_tag(self):
        return self.__tag

    def get_value(self):
        return self.__value

    def get_line_content(self):
        return self.__line_content

    def set_content(self, value):
        self.__content = value

    def set_gedcom_index(self, value):
        self.__gedcom_index = value

    def set_level(self, value):
        self.__level = value

    def set_pointer(self, value):
        self.__pointer = value

    def set_tag(self, value):
        self.__tag = value

    def set_value(self, value):
        self.__value = value

    def set_line_content(self, value):
        self.__line_content = value

    def del_content(self):
        del self.__content

    def del_gedcom_index(self):
        del self.__gedcom_index

    def del_level(self):
        del self.__level

    def del_pointer(self):
        del self.__pointer

    def del_tag(self):
        del self.__tag

    def del_value(self):
        del self.__value

    def del_line_content(self):
        del self.__line_content
        
    def __str__(self):
        return self.__line_content

    def __repr__(self):
        return self.__line_content
    
    content = property(get_content, set_content, del_content, "content's docstring")
    gedcom_index = property(get_gedcom_index, set_gedcom_index, del_gedcom_index, "gedcom_index's docstring")
    level = property(get_level, set_level, del_level, "level's docstring")
    pointer = property(get_pointer, set_pointer, del_pointer, "pointer's docstring")
    tag = property(get_tag, set_tag, del_tag, "tag's docstring")
    value = property(get_value, set_value, del_value, "value's docstring")
    line_content = property(get_line_content, set_line_content, del_line_content, "line_content's docstring")
