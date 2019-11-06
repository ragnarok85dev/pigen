#
# GEDCOM 5.5 standard tags
#

# ABBREVIATION
# A short name of a title, description, or name.
GEDCOM_TAG_NAME_ABBREVIATION = "ABBR"

# ADDRESS
# The contemporary place, usually required for postal purposes, of an individual, a submitter of information, a repository, a business, a school, or a company.
GEDCOM_TAG_ADDRESS = "ADDR"

# ADDRESS1
# The first line of an address.
GEDCOM_TAG_ADDRESS_LINE1 = "ADR1"

# ADDRESS2
# The second line of an address.
GEDCOM_TAG_ADDRESS_LINE2 = "ADR2"

# ADDRESS3
# The second line of an address.
GEDCOM_TAG_ADDRESS_LINE3 = "ADR3"

# ADOPTION
# Pertaining to creation of a child-parent relationship that does not exist biologically.
GEDCOM_TAG_ADOPTION = "ADOP"

# AFN
# Ancestral File Nummer, a unique permanent record file number of an individual record stored in Ancestral File.
GEDCOM_TAG_ANCESTRAL_FILE_NUMBER = "AFN"

# AGE
# The age of the individual at the time an event occurred, or the age listed in the document.
GEDCOM_TAG_AGE = "AGE"

# AGENCY
# The institution or individual having authority and/or responsibility to manage or govern.
GEDCOM_TAG_AGENCY = "AGNC"

# ALIAS
# An indicator to link different record descriptions of a person who may be the same person.
GEDCOM_TAG_ALIAS = "ALIA"

# ANCESTORS
# Pertaining to forbearers of an individual.
GEDCOM_TAG_ANCESTORS = "ANCE"

# ANCES_INTEREST
# Indicates an interest in additional research for ancestors of this individual. (See also DESI)
GEDCOM_TAG_ANCES_INTEREST = "ANCI"

# ANNULMENT
# Declaring a marriage void from the beginning (never existed).
GEDCOM_TAG_MARIAGE_ANNULMENT = "ANUL"

# ASSOCIATES
# An indicator to link friends, neighbors, relatives, or associates of an individual.
GEDCOM_TAG_ASSOCIATES = "ASSO"

# AUTHOR
# The name of the individual who created or compiled information.
GEDCOM_TAG_AUTHOR = "AUTH"

# BAPTISM-LDS
# The event of baptism performed at age eight or later by priesthood authority of the LDS Church. (See also BAPM)
GEDCOM_TAG_LDS_BAPTIST = "BAPL"

# BAPTISM
# The event of baptism (not LDS), performed in infancy or later. (See also BAPL and CHR)
GEDCOM_TAG_BAPTISM = "BAPM"

# BAR_MITZVAH
# The ceremonial event held when a Jewish boy reaches age 13.
GEDCOM_TAG_BAR_MITZVAH = "BARM"

# BAS_MITZVAH
# The ceremonial event held when a Jewish girl reaches age 13, also known as "Bat Mitzvah."
GEDCOM_TAG_BAS_MITZVAH = "BASM"

# BIRTH
# The event of entering into life.
GEDCOM_TAG_BIRTH = "BIRT"

# BLESSING
# A religious event of bestowing divine care or intercession. Sometimes given in connection with a naming ceremony.
GEDCOM_TAG_BLESSING = "BLES"

# BURIAL
# The event of the proper disposing of the mortal remains of a deceased person.
GEDCOM_TAG_BURIAL = "BURI"

# CALL_NUMBER
# The number used by a repository to identify the specific items in its collections.
GEDCOM_TAG_CALL_NUMBER = "CALN"

# CASTE
# The name of an individual's rank or status in society, based on racial or religious differences, or differences in wealth, inherited rank, profession, occupation, etc.
GEDCOM_TAG_CASTE = "CAST"

# CAUSE
# A description of the cause of the associated event or fact, such as the cause of death.
GEDCOM_TAG_CAUSE = "CAUS"

# CENSUS
# The event of the periodic count of the population for a designated locality, such as a national or state Census.
GEDCOM_TAG_CENSUS = "CENS"

# CHANGE
# Indicates a change, correction, or modification. Typically used in connection with a DATE to specify when a change in information occurred.
GEDCOM_TAG_DATE_CHANGE = "CHAN"

# CHARACTER
# An indicator of the character set used in writing this automated information.
GEDCOM_TAG_CHARACTER_SET = "CHAR"

# CHILD
# The natural, adopted, or sealed (LDS) child of a father and a mother.
GEDCOM_TAG_CHILD = "CHIL"

# CHRISTENING
# The religious event (not LDS) of baptizing and/or naming a child.
GEDCOM_TAG_CHRISTENING = "CHR"

# ADULT_CHRISTENING
# The religious event (not LDS) of baptizing and/or naming an adult person.
GEDCOM_TAG_ADULT_CHRISTENING = "CHRA"

# CITY
# A lower level jurisdictional unit. Normally an incorporated municipal unit.
GEDCOM_TAG_CITY = "CITY"

# CONCATENATION
# An indicator that additional data belongs to the superior value. The information from the CONC value is to be connected to the value of the superior preceding line without a space and without a carriage return and/or new line character. Values that are split for a CONC tag must always be split at a non-space. If the value is split on a space the space will be lost when concatenation takes place. This is because of the treatment that spaces get as a GEDCOM delimiter, many GEDCOM values are trimmed of trailing spaces and some systems look for the first non-space starting after the tag to determine the beginning of the value.
GEDCOM_TAG_CONCATENATION = "CONC"

# CONFIRMATION
# The religious event (not LDS) of conferring the gift of the Holy Ghost and, among protestants, full church membership.
GEDCOM_TAG_CONFIRMATION = "CONF"

# CONFIRMATION_L
# The religious event by which a person receives membership in the LDS Church.
GEDCOM_TAG_LSD_CONFIRMATION = "CONL"

# CONTINUED
# An indicator that additional data belongs to the superior value. The information from the CONT value is to be connected to the value of the superior preceding line with a carriage return and/or new line character. Leading spaces could be important to the formatting of the resultant text. When importing values from CONT lines the reader should assume only one delimiter character following the CONT tag. Assume that the rest of the leading spaces are to be a part of the value.
GEDCOM_TAG_CONTINUED = "CONT"

# COPYRIGHT
# A statement that accompanies data to protect it from unlawful duplication and distribution.
GEDCOM_TAG_COPYRIGHT = "COPR"

# CORPORATE
# A name of an institution, agency, corporation, or company.
GEDCOM_TAG_CORPORATE = "CORP"

# CREMATION
# Disposal of the remains of a person's body by fire.
GEDCOM_TAG_CREMATION = "CREM"

# COUNTRY
# The name or code of the country.
GEDCOM_TAG_COUNTRY = "CTRY"

# DATA
# Pertaining to stored automated information.
GEDCOM_TAG_DATA = "DATA"

# DATE
# The time of an event in a calendar format.
GEDCOM_TAG_DATE = "DATE"

# DEATH
# The event when mortal life terminates.
GEDCOM_TAG_DEATH = "DEAT"

# DESCENDANTS
# Pertaining to offspring of an individual.
GEDCOM_TAG_DESCENDANTS = "DESC"

# DESCENDANT_INT
# Indicates an interest in research to identify additional descendants of this individual. (See also ANCI)
GEDCOM_TAG_DESCENDANT_INT = "DESI"

# DESTINATION
# A system receiving data.
GEDCOM_TAG_DESTINATION = "DEST"

# DIVORCE
# An event of dissolving a marriage through civil action.
GEDCOM_TAG_DIVORCE = "DIV"

# DIVORCE_FILED
# An event of filing for a divorce by a spouse.
GEDCOM_TAG_DIVORCE_FILED = "DIVF"

# PHY_DESCRIPTION
# The physical characteristics of a person, place, or thing.
GEDCOM_TAG_PHYSICAL_DESCRIPTION = "DSCR"

# EDUCATION
# Indicator of a level of education attained.
GEDCOM_TAG_EDUCATION = "EDUC"

# EMAIL
# An electronic address that can be used for contact such as an email address... 
GEDCOM_TAG_EMAIL = "EMAIL"

# EMIGRATION
# An event of leaving one's homeland with the intent of residing elsewhere.
GEDCOM_TAG_EMIGRATION = "EMIG"

# ENDOWMENT
# A religious event where an endowment ordinance for an individual was performed by priesthood authority in an LDS temple.
GEDCOM_TAG_LSD_ENDOWMENT = "ENDL"

# ENGAGEMENT
# An event of recording or announcing an agreement between two people to become married.
GEDCOM_TAG_ENGAGEMENT = "ENGA"

# EVENT
# A noteworthy happening related to an individual, a group, or an organization.
GEDCOM_TAG_EVENT = "EVEN"

# FACT
# Pertaining to a noteworthy attribute or fact concerning an individual, a group, or an organization. A
GEDCOM_TAG_FACT = "FACT"

# FAMILY
# Identifies a legal, common law, or other customary relationship of man and woman and their children, if any, or a family created by virtue of the birth of a child to its biological father and mother.
GEDCOM_TAG_FAMILY = "FAM"

# FAMILY_CHILD
# Identifies the family in which an individual appears as a child.
GEDCOM_TAG_FAMILY_CHILD = "FAMC"

# FAMILY_FILE
# Pertaining to, or the name of, a family file. Names stored in a file that are assigned to a family for doing temple ordinance work.
GEDCOM_TAG_FAMILY_FILE = "FAMF"

# FAMILY_SPOUSE
# Identifies the family in which an individual appears as a spouse.
GEDCOM_TAG_FAMILY_SPOUSE = "FAMS"

# FAX
# A FAX telephone number appropriate for sending data facsimiles. 
GEDCOM_TAG_FAX = "FAX"

# FIRST_COMMUNION
# A religious rite, the first act of sharing in the Lord's supper as part of church worship.
GEDCOM_TAG_FIRST_COMMUNION = "FCOM"

# FILE
# An information storage place that is ordered and arranged for preservation and reference.
GEDCOM_TAG_FILE = "FILE"

# PHONETIC
# A phonetic variation of a superior text string. 
GEDCOM_TAG_PHONETIC = "FONE"

# FORMAT
# An assigned name given to a consistent format in which information can be conveyed.
GEDCOM_TAG_FORMAT = "FORM"

# GEDCOM
# Information about the use of GEDCOM in a transmission.
GEDCOM_TAG_GEDCOM = "GEDC"

# GIVEN_NAME
# A given or earned name used for official identification of a person.
GEDCOM_TAG_GIVEN_NAME = "GIVN"

# GRADUATION
# An event of awarding educational diplomas or degrees to individuals.
GEDCOM_TAG_GRADUATION = "GRAD"

# HEADER
# Identifies information pertaining to an entire GEDCOM transmission.
GEDCOM_TAG_HEADER = "HEAD"

# HUSBAND
# An individual in the family role of a married man or father.
GEDCOM_TAG_HUSBAND = "HUSB"

# IDENT_NUMBER
# A number assigned to identify a person within some significant external system.
GEDCOM_TAG_IDENT_NUMBER = "IDNO"

# IMMIGRATION
# An event of entering into a new locality with the intent of residing there.
GEDCOM_TAG_IMMIGRATION = "IMMI"

# INDIVIDUAL
# A person.
GEDCOM_TAG_INDIVIDUAL = "INDI"

# LANGUAGE
# The name of the language used in a communication or transmission of information.
GEDCOM_TAG_LANGUAGE = "LANG"

# LATITUDE
# A value indicating a coordinate position on a line, plane, or space. 
GEDCOM_TAG_LATITUDE = "LATI"

# LEGATEE
# A role of an individual acting as a person receiving a bequest or legal devise.
GEDCOM_TAG_LEGATEE = "LEGA"

# LONGITUDE
# A value indicating a coordinate position on a line, plane, or space. 
GEDCOM_TAG_LONGITUDE = "LONG"

# MAP
# Pertains to a representation of measurements usually presented in a graphical form. 
GEDCOM_TAG_MAP = "MAP"

# MARRIAGE_BANN
# An event of an official public notice given that two people intend to marry.
GEDCOM_TAG_MARRIAGE_BANN = "MARB"

# MARR_CONTRACT
# An event of recording a formal agreement of marriage, including the prenuptial agreement in which marriage partners reach agreement about the property rights of one or both, securing property to their children.
GEDCOM_TAG_MARR_CONTRACT = "MARC"

# MARR_LICENSE
# An event of obtaining a legal license to marry.
GEDCOM_TAG_MARR_LICENSE = "MARL"

# MARRIAGE
# A legal, common-law, or customary event of creating a family unit of a man and a woman as husband and wife.
GEDCOM_TAG_MARRIAGE = "MARR"

# MARR_SETTLEMENT
# An event of creating an agreement between two people contemplating marriage, at which time they agree to release or modify property rights that would otherwise arise from the marriage.
GEDCOM_TAG_MARR_SETTLEMENT = "MARS"

# MEDIA
# Identifies information about the media or having to do with the medium in which information is stored.
GEDCOM_TAG_MEDIA = "MEDI"

# NAME
# A word or combination of words used to help identify an individual, title, or other item. More than one NAME line should be used for people who were known by multiple names.
GEDCOM_TAG_NAME = "NAME"

# NATIONALITY
# The national heritage of an individual.
GEDCOM_TAG_NATIONALITY = "NATI"

# NATURALIZATION
# The event of obtaining citizenship.
GEDCOM_TAG_NATURALIZATION = "NATU"

# CHILDREN_COUNT
# The number of children that this person is known to be the parent of (all marriages) when subordinate to an individual, or that belong to this family when subordinate to a FAM_RECORD.
GEDCOM_TAG_CHILDREN_COUNT = "NCHI"

# NICKNAME
# A descriptive or familiar that is used instead of, or in addition to, one's proper name.
GEDCOM_TAG_NICKNAME = "NICK"

# MARRIAGE_COUNT
# The number of times this person has participated in a family as a spouse or parent.
GEDCOM_TAG_MARRIAGE_COUNT = "NMR"

# NOTE
# Additional information provided by the submitter for understanding the enclosing data.
GEDCOM_TAG_NOTE = "NOTE"

# NAME_PREFIX
# Text which appears on a name line before the given and surname parts of a name. i.e. ( Lt. Cmndr. ) Joseph /Allen/ jr. In this example Lt. Cmndr. is considered as the name prefix portion.
GEDCOM_TAG_NAME_PREFIX = "NPFX"

# NAME_SUFFIX
# Text which appears on a name line after or behind the given and surname parts of a name. i.e. Lt. Cmndr. Joseph /Allen/ ( jr. ) In this example jr. is considered as the name suffix portion.
GEDCOM_TAG_NAME_SUFFIX = "NSFX"

# OBJECT
# Pertaining to a grouping of attributes used in describing something. Usually referring to the data required to represent a multimedia object, such an audio recording, a photograph of a person, or an image of a document.
GEDCOM_TAG_OBJECT = "OBJE"

# OCCUPATION
# The type of work or profession of an individual.
GEDCOM_TAG_OCCUPATION = "OCCU"

# ORDINANCE
# Pertaining to a religious ordinance in general.
GEDCOM_TAG_ORDINANCE = "ORDI"

# ORDINATION
# A religious event of receiving authority to act in religious matters.
GEDCOM_TAG_ORDINATION = "ORDN"

# PAGE
# A number or description to identify where information can be found in a referenced work.
GEDCOM_TAG_PAGE = "PAGE"

# PEDIGREE
# Information pertaining to an individual to parent lineage chart.
GEDCOM_TAG_PEDIGREE = "PEDI"

# PHONE
# A unique number assigned to access a specific telephone.
GEDCOM_TAG_PHONE = "PHON"

# PLACE
# A jurisdictional name to identify the place or location of an event.
GEDCOM_TAG_PLACE = "PLAC"

# POSTAL_CODE
# A code used by a postal service to identify an area to facilitate mail handling.
GEDCOM_TAG_POSTAL_CODE = "POST"

# PROBATE
# An event of judicial determination of the validity of a will. May indicate several related court activities over several dates.
GEDCOM_TAG_PROBATE = "PROB"

# PROPERTY
# Pertaining to possessions such as real estate or other property of interest.
GEDCOM_TAG_PROPERTY = "PROP"

# PUBLICATION
# Refers to when and/or were a work was published or created.
GEDCOM_TAG_PUBLICATION = "PUBL"

# QUALITY_OF_DATA
# An assessment of the certainty of the evidence to support the conclusion drawn from evidence.
GEDCOM_TAG_QUALITY_OF_DATA = "QUAY"

# REFERENCE
# A description or number used to identify an item for filing, storage, or other reference purposes.
GEDCOM_TAG_REFERENCE = "REFN"

# RELATIONSHIP
# A relationship value between the indicated contexts.
GEDCOM_TAG_RELATIONSHIP = "RELA"

# RELIGION
# A religious denomination to which a person is affiliated or for which a record applies.
GEDCOM_TAG_RELIGION = "RELI"

# REPOSITORY
# An institution or person that has the specified item as part of their collection(s).
GEDCOM_TAG_REPOSITORY = "REPO"

# RESIDENCE
# The act of dwelling at an address for a period of time.
GEDCOM_TAG_RESIDENCE = "RESI"

# RESTRICTION
# A processing indicator signifying access to information has been denied or otherwise restricted.
GEDCOM_TAG_RESTRICTION = "RESN"

# RETIREMENT
# An event of exiting an occupational relationship with an employer after a qualifying time period.
GEDCOM_TAG_RETIREMENT = "RETI"

# REC_FILE_NUMBER
# A permanent number assigned to a record that uniquely identifies it within a known file.
GEDCOM_TAG_REC_FILE_NUMBER = "RFN"

# REC_ID_NUMBER
# A number assigned to a record by an originating automated system that can be used by a receiving system to report results pertaining to that record.
GEDCOM_TAG_REC_ID_NUMBER = "RIN"

# ROLE
# A name given to a role played by an individual in connection with an event.
GEDCOM_TAG_ROLE = "ROLE"

# ROMANIZED
# A romanized variation of a superior text string. 
GEDCOM_TAG_ROMANIZED = "ROMN"

# SEX
# Indicates the sex of an individual--male or female.
GEDCOM_TAG_SEX = "SEX"

# SEALING_CHILD
# A religious event pertaining to the sealing of a child to his or her parents in an LDS temple ceremony.
GEDCOM_TAG_LSD_SEALING_CHILD = "SLGC"

# SEALING_SPOUSE
# A religious event pertaining to the sealing of a husband and wife in an LDS temple ceremony.
GEDCOM_TAG_LSD_SEALING_SPOUSE = "SLGS"

# SOURCE
# The initial or original material from which information was obtained.
GEDCOM_TAG_SOURCE = "SOUR"

# SURN_PREFIX
# A name piece used as a non-indexing pre-part of a surname.
GEDCOM_TAG_SURN_PREFIX = "SPFX"

# SOC_SEC_NUMBER
# A number assigned by the United States Social Security Administration. Used for tax identification purposes.
GEDCOM_TAG_SOC_SEC_NUMBER = "SSN"

# STATE
# A geographical division of a larger jurisdictional area, such as a State within the United States of America.
GEDCOM_TAG_STATE = "STAE"

# STATUS
# An assessment of the state or condition of something.
GEDCOM_TAG_STATUS = "STAT"

# SUBMITTER
# An individual or organization who contributes genealogical data to a file or transfers it to someone else.
GEDCOM_TAG_SUBMITTER = "SUBM"

# SUBMISSION
# Pertains to a collection of data issued for processing.
GEDCOM_TAG_SUBMISSION = "SUBN"

# SURNAME
# A family name passed on or used by members of a family.
GEDCOM_TAG_SURNAME = "SURN"

# TEMPLE
# The name or code that represents the name a temple of the LDS Church.
GEDCOM_TAG_LSD_TEMPLE = "TEMP"

# TEXT
# The exact wording found in an original source document.
GEDCOM_TAG_TEXT = "TEXT"

# TIME
# A time value in a 24-hour clock format, including hours, minutes, and optional seconds, separated by a colon (:). Fractions of seconds are shown in decimal notation.
GEDCOM_TAG_TIME = "TIME"

# TITLE
# A description of a specific writing or other work, such as the title of a book when used in a source context, or a formal designation used by an individual in connection with positions of royalty or other social status, such as Grand Duke.
GEDCOM_TAG_TITLE = "TITL"

# TRAILER
# At level 0, specifies the end of a GEDCOM transmission.
GEDCOM_TAG_TRAILER = "TRLR"

# TYPE
# A further qualification to the meaning of the associated superior tag. The value does not have any computer processing reliability. It is more in the form of a short one or two word note that should be displayed any time the associated data is displayed.
GEDCOM_TAG_TYPE = "TYPE"

# VERSION
# Indicates which version of a product, item, or publication is being used or referenced.
GEDCOM_TAG_VERSION = "VERS"

# WIFE
# An individual in the role as a mother and/or married woman.
GEDCOM_TAG_WIFE = "WIFE"

# WEB
# World Wide Web home page. 
GEDCOM_TAG_WEB = "WWW"

# WILL
# A legal document treated as an event, by which a person disposes of his or her estate, to take effect after death. The event date is the date the will was signed while the person was alive. (See also PROBate)
GEDCOM_TAG_WILL = "WILL"



#
# PIGEN custom tags and list of tags
#
INDIVIDUAL_NAME_UNKNOWN = "<Sconosciuto>"

MAX_TEXT_LENGTH = 200

PERSONAL_NAME_PIECES_TAGS = [GEDCOM_TAG_NAME_PREFIX,
                             GEDCOM_TAG_GIVEN_NAME,
                             GEDCOM_TAG_NICKNAME,
                             GEDCOM_TAG_SURN_PREFIX,
                             GEDCOM_TAG_SURNAME,
                             GEDCOM_TAG_NAME_SUFFIX,
                             GEDCOM_TAG_NOTE,
                             GEDCOM_TAG_SOURCE]

FAMILY_EVENT_STRUCTURE_TAGS = [GEDCOM_TAG_MARIAGE_ANNULMENT, 
                                GEDCOM_TAG_CENSUS, 
                                GEDCOM_TAG_DIVORCE, 
                                GEDCOM_TAG_DIVORCE_FILED, 
                                GEDCOM_TAG_ENGAGEMENT, 
                                GEDCOM_TAG_MARRIAGE_BANN, 
                                GEDCOM_TAG_MARR_CONTRACT,
                                GEDCOM_TAG_MARR_LICENSE, 
                                GEDCOM_TAG_MARR_SETTLEMENT, 
                                GEDCOM_TAG_RESIDENCE,
                                GEDCOM_TAG_EVENT,
                                GEDCOM_TAG_MARRIAGE]

INDIVIDUAL_EVENT_STRUCTURE_TAGS = [GEDCOM_TAG_BIRTH, 
                                   GEDCOM_TAG_CHRISTENING,
                                   GEDCOM_TAG_DEATH,
                                   GEDCOM_TAG_ADOPTION,
                                   GEDCOM_TAG_BURIAL,
                                   GEDCOM_TAG_CREMATION,
                                   GEDCOM_TAG_BAPTISM,
                                   GEDCOM_TAG_BAR_MITZVAH,
                                   GEDCOM_TAG_BAS_MITZVAH,
                                   GEDCOM_TAG_BLESSING,
                                   GEDCOM_TAG_ADULT_CHRISTENING,
                                   GEDCOM_TAG_CONFIRMATION,
                                   GEDCOM_TAG_FIRST_COMMUNION,
                                   GEDCOM_TAG_ORDINATION,
                                   GEDCOM_TAG_NATURALIZATION,
                                   GEDCOM_TAG_EMIGRATION,
                                   GEDCOM_TAG_IMMIGRATION,
                                   GEDCOM_TAG_CENSUS,
                                   GEDCOM_TAG_PROBATE,
                                   GEDCOM_TAG_WILL,
                                   GEDCOM_TAG_GRADUATION,
                                   GEDCOM_TAG_RETIREMENT,
                                   GEDCOM_TAG_EVENT]

INDIVIDUAL_ATTRIBUTE_STRUCTURE_TAGS = [GEDCOM_TAG_PHYSICAL_DESCRIPTION,
                                       GEDCOM_TAG_CASTE,
                                       GEDCOM_TAG_EDUCATION,
                                       GEDCOM_TAG_IDENT_NUMBER,
                                       GEDCOM_TAG_NATIONALITY,
                                       GEDCOM_TAG_CHILDREN_COUNT,
                                       GEDCOM_TAG_MARRIAGE_COUNT,
                                       GEDCOM_TAG_OCCUPATION,
                                       GEDCOM_TAG_PROPERTY,
                                       GEDCOM_TAG_RELIGION,
                                       GEDCOM_TAG_RESIDENCE,
                                       GEDCOM_TAG_SOC_SEC_NUMBER,
                                       GEDCOM_TAG_TITLE,
                                       GEDCOM_TAG_FACT]

EVENT_DETAIL_TAGS = [GEDCOM_TAG_TYPE,
                     GEDCOM_TAG_DATE,
                     GEDCOM_TAG_PLACE,
                     GEDCOM_TAG_ADDRESS,
                     GEDCOM_TAG_AGENCY,
                     GEDCOM_TAG_RELIGION,
                     GEDCOM_TAG_CAUSE,
                     GEDCOM_TAG_RESTRICTION,
                     GEDCOM_TAG_NOTE,
                     GEDCOM_TAG_SOURCE,
                     GEDCOM_TAG_OBJECT]

IGNORED_INDIVIDUAL_RECORD_TAGS = [GEDCOM_TAG_ASSOCIATES,
                                  GEDCOM_TAG_LDS_BAPTIST,
                                  GEDCOM_TAG_LSD_CONFIRMATION,
                                  GEDCOM_TAG_LSD_ENDOWMENT,
                                  GEDCOM_TAG_LSD_SEALING_CHILD]

IGNORED_FAMILY_RECORD_TAGS = [GEDCOM_TAG_LSD_SEALING_SPOUSE]