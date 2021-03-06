#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================
#
#
#   glinter.py
#   Glyph name validity testing script
#   Copyright 2018 Christopher Simpkins
#   Apache License 2.0
#
#   Version 0.3.1
#
# ==============================================================

# USAGE
#
# This script is dependent upon the Python 3 interpreter.  If a Python 3 interpreter
# is not available on your system, please see the Python documentation at
# https://www.python.org/downloads/ for instructions on how to install it.
#
#
# Execute the script from any directory on your system by passing one or more
# filepath arguments to local filter list definition files on your system:
#
#    $ python3 glinter.py [filepath 1] [filepath ...]
#
# The script tests each glyph name listed in the definition file vs.
# the Glyphs application GlyphData.xml file and Adobe OpenType
# Feature File specification for development glyph names
#
# Glyph names are tested against the Glyphs GlyphData.xml file to determine
# if they are:
#   - Glyphs-defined nice names (AGL style names)
#   - Glyphs-defined Unicode hexadecimal style names (e.g, uniXXXX, uXXXXX)
#   - common alternate names -- if found, the above two glyph names are suggested
#
# If the glyph name is not found in the above set of lists, the script will raise
# an error and identify the definition file path where the error was found.
#
# For glyph names that pass the above tests, the following additional tests
# that are based upon the Adobe OT Feature File spec are performed:
#    - glyph name < 64 characters in length
#    - glyph name does not contain a leading period (except .notdef and .null)
#    - glyph name contains valid characters for development glyph names
#
# Adobe reference:
#  https://github.com/adobe-type-tools/afdko/blob/develop/docs/OpenTypeFeatureFileSpecification.html

import os
import re
import sys
import xml.etree.ElementTree as ET


class Glyph(object):
    def __init__(self):
        self.unicode = ""
        self.name = ""
        self.description = ""
        self.production = ""
        self.alt_names = []


class Filter(object):
    """Filter is an object that maintains data elements for Glyphs application filter lists.
       It is instantiated with a new filter list name and list elements are defined with
       a class method"""

    def __init__(self, name):
        self.comment_delimiters = ("#", "/")
        self.name = name
        self.list = []

    def define_list_with_newline_delimited_text(self, text):
        """Filter class method that defines a Filter object with parsed data from newline-
           delimited text files of list elements"""
        raw_code_point_list = text.splitlines()
        filtered_code_point_list = []
        for item in raw_code_point_list:
            test_item = item.strip()
            if len(test_item) == 0:  # discard blank lines in definition file
                pass
            elif (
                test_item[0] in self.comment_delimiters
            ):  # discard comment lines in definition file
                pass
            else:
                filtered_code_point_list.append(test_item)
        self.list = filtered_code_point_list


def main(argv):
    # parse GlyphData.xml file for Glyphs application supported glyph name values
    glyphlist = []
    unicode_set = set()
    name_set = set()
    production_set = set()
    altname_set = set()

    tree = ET.parse(
        "/Applications/Glyphs.app/Contents/Frameworks/GlyphsCore.framework/Versions/A/Resources/GlyphData.xml"
    )
    root = tree.getroot()
    for child in root:
        glyph = Glyph()
        if "unicode" in child.attrib:
            glyph.unicode = child.attrib["unicode"]
            unicode_set.add(glyph.unicode)
        if "name" in child.attrib:
            glyph.name = child.attrib["name"]
            name_set.add(glyph.name)
        if "description" in child.attrib:
            glyph.description = child.attrib["description"]
        if "production" in child.attrib:
            glyph.production = child.attrib["production"]
            production_set.add(glyph.production)
        if "altNames" in child.attrib:
            namestring = child.attrib["altNames"]
            if len(namestring) > 0:
                name_list = namestring.split(",")
                for altname in name_list:
                    save_name = altname.strip()
                    glyph.alt_names.append(save_name)
                    altname_set.add(save_name)

        glyphlist.append(glyph)

    # parse filter list definition files that were passed as command line args
    filter_list = []

    for filepath in argv:
        if os.path.isfile(filepath):
            new_filter = Filter(filepath)
            with open(filepath) as f:
                text = f.read()
                new_filter.define_list_with_newline_delimited_text(text)
                filter_list.append(new_filter)
        else:
            sys.stderr.write(
                "[ERROR]: Unable to identify a file on the path '"
                + filepath
                + "'"
                + os.linesep
            )

    if len(filter_list) == 0:
        sys.stderr.write(
            "[ERROR]: Unable to identify any definitions in the requested files!"
            + os.linesep
        )
        sys.exit(1)

    # BEGIN TESTS
    ANY_ERROR_DETECTED = False
    for a_filter in filter_list:
        FILTER_ERROR_DETECTED = False
        for glyph_name in a_filter.list:
            if glyph_name in name_set:
                pass
            elif glyph_name in production_set:
                pass
            elif glyph_name in altname_set:
                ANY_ERROR_DETECTED = True
                FILTER_ERROR_DETECTED = True
                sys.stderr.write(
                    "'"
                    + glyph_name
                    + "' in definition file '"
                    + a_filter.name
                    + "' appears to be an alternate name.  Consider replacement with one of the following names:"
                    + os.linesep
                )
                for a_glyph in glyphlist:
                    if glyph_name in a_glyph.alt_names:
                        if len(a_glyph.name) > 0:
                            sys.stderr.write(" --> " + a_glyph.name + os.linesep)
                        if len(a_glyph.production) > 0:
                            sys.stderr.write(" --> " + a_glyph.production + os.linesep)
                        if len(a_glyph.unicode) == 4:
                            uni_name = "uni" + a_glyph.unicode
                            if not uni_name == a_glyph.production:
                                sys.stderr.write(" --> " + uni_name + os.linesep)
                        elif len(a_glyph.unicode) == 5:
                            uni_name = "u" + a_glyph.unicode
                            if not uni_name == a_glyph.production:
                                sys.stderr.write(" --> " + uni_name + os.linesep)
            else:
                sys.stderr.write(
                    "'"
                    + glyph_name
                    + "' does not appear to be a valid glyph name!"
                    + os.linesep
                )
                ANY_ERROR_DETECTED = True
                FILTER_ERROR_DETECTED = True

            # BEGIN non-GlyphData.xml tests
            if FILTER_ERROR_DETECTED is False:
                # https://github.com/adobe-type-tools/afdko/blob/develop/docs/OpenTypeFeatureFileSpecification.html
                # glyph name length
                if len(glyph_name) > 63:
                    sys.stderr.write(
                        "'" + glyph_name + "' is too long! (> 63 characters)"
                    )
                    FILTER_ERROR_DETECTED = True
                    ANY_ERROR_DETECTED = True
                # glyph name starts with period outside of defined positions (including .null defined in GlyphData.xml)
                if glyph_name[0] == "." and (glyph_name not in (".notdef", ".null")):
                    sys.stderr.write(
                        "'" + glyph_name + "' includes an invalid leading period!"
                    )
                    FILTER_ERROR_DETECTED = True
                    ANY_ERROR_DETECTED = True

                # glyph name contains valid characters
                if not has_valid_characters(glyph_name):
                    sys.stderr.write(
                        "'" + glyph_name + "' contains invalid characters!" + os.linesep
                    )
                    FILTER_ERROR_DETECTED = True
                    ANY_ERROR_DETECTED = True

        if FILTER_ERROR_DETECTED is True:
            sys.stderr.write("[ERROR] --> " + a_filter.name + os.linesep)
        else:
            print("[OK] " + a_filter.name)

    if ANY_ERROR_DETECTED is True:
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)


def has_valid_characters(glyph_name):
    """Tests for presence of valid characters in a glyph name as specified by the Adobe
       OpenType Feature File specification.  The test here includes characters
       specified for 'development' names, a broader set than the production name
       definition

       https://github.com/adobe-type-tools/afdko/blob/develop/docs/OpenTypeFeatureFileSpecification.html"""
    valid_characters = r"^[A-Za-z0-9\._\*\+\-\:\^\|\~]{1,63}$"
    regex = re.compile(valid_characters)
    return re.match(regex, glyph_name)


if __name__ == "__main__":
    main(sys.argv[1:])
