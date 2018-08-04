#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ===========================================================
#
#
#   exportfilters.py
#   A Glyphs font editor filter list to FLM plugin
#     definition file exporter script
#   Copyright 2018 Christopher Simpkins
#   Apache License 2.0
#
#   Version 0.1.1
#
# ===========================================================

# USAGE
#
# This script is dependent upon the Python 3 interpreter.  If a Python 3 interpreter
# is not available on your system, please see the Python documentation at
# https://www.python.org/downloads/ for instructions on how to install it.
#
#
# Execute the script from any directory on your system with the following command
# in your terminal window:
#
#    python3 exportfilters.py
#
#
# Following execution your existing Glyphs application filter lists will be
# exported as newline delimited definition files that are formatted so that
# they work with the Filter List Manager plugin.  The filter list name is
# mapped to the base file name of the definition file and the glyph definitions
# are listed with newline separators.  You can find all definition files on
# the path ~/GlyphsFilters.

import os
import plistlib
import sys


def main():
    try:
        # default paths
        glyphs_plist_path = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Glyphs",
            "CustomFilter.plist",
        )

        flm_definitions_directory_path = os.path.join(
            os.path.expanduser("~"), "GlyphsFilters"
        )

        if not os.path.isdir(flm_definitions_directory_path):
            os.makedirs(flm_definitions_directory_path)

        with open(glyphs_plist_path, "rb") as f:
            filters_data = plistlib.load(f)
            for filter_dict in filters_data:
                if "list" in filter_dict:
                    # define filter file name and filter list contents
                    filter_name = filter_dict["name"]
                    filter_list = filter_dict["list"]

                    base_filepath = filter_name + ".txt"
                    outfile_path = os.path.join(
                        flm_definitions_directory_path, base_filepath
                    )

                    # create newline-delimited file format
                    outfile_text = (
                        "// " + filter_name + " filter" + os.linesep + os.linesep
                    )
                    for glyph_name in filter_list:
                        outfile_text += glyph_name + os.linesep

                    with open(outfile_path, "w") as w:
                        w.write(outfile_text)
                        print(filter_name + " filter list exported...")

        print("---")
        print("Export complete!")
        print("You can find the definition files in the directory ~/GlyphsFilters")
    except Exception as e:
        sys.stderr.write(
            "[ERROR] There was an error during the export attempt. "
            + str(e)
            + os.linesep
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
