# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#   Filter List Manager
#   A plugin for the Glyphs font editor
#   Copyright 2018 Christopher Simpkins
#   Apache License 2.0
#
#
###########################################################################################################

import logging
import objc
import os
import plistlib
import shutil
import subprocess
try:
	import urllib2 as urllibrequest
	import urlparse as urllibparse
except:
	import urllib.request as urllibrequest
	import urllib.parse as urllibparse

from GlyphsApp import *
from GlyphsApp.plugins import *

# -----------------
# Path definitions
# -----------------
# Glyphs application paths
GLYPHS_PLIST_FILE = os.path.join(
    os.path.expanduser("~"),
    "Library",
    "Application Support",
    "Glyphs",
    "CustomFilter.plist",
)


# FLM plugin paths
FLM_GLYPHSFILTERS_DIR = os.path.join(os.path.expanduser("~"), "GlyphsFilters")
FLM_BACKUP_DIR = os.path.join(os.path.expanduser("~"), "GlyphsFilters", "backup")
FLM_BACKUP_ORIGINAL_FILE = os.path.join(FLM_BACKUP_DIR, "CustomFilters.plist.original")
FLM_BACKUP_PREVIOUS_FILE = os.path.join(FLM_BACKUP_DIR, "CustomFilters.plist")
FLM_DEFAULT_PLIST = os.path.join(
    os.path.expanduser("~"),
    "Library",
    "Application Support",
    "Glyphs",
    "Plugins",
    "FilterListManager.glyphsPlugin",
    "Contents",
    "Resources",
    "CustomFilter.plist",
)
FLM_LOG_DIR = os.path.join(os.path.expanduser("~"), "GlyphsFilters", "logs")
FLM_LOG_FILE = os.path.join(FLM_LOG_DIR, "flm.log")
FLM_REMOTE_DEF_FILE = os.path.join(
    os.path.expanduser("~"), "GlyphsFilters", "remote", "defs.txt"
)

# ---------------
# Logging setup
# ---------------
if not os.path.isdir(FLM_LOG_DIR):
    os.makedirs(FLM_LOG_DIR)
logging.basicConfig(
    filename=FLM_LOG_FILE,
    filemode="w",
    format="%(asctime)s %(levelname)s  %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)

# ----------------------------
# CustomFilters.plist backup
# ----------------------------
# Backup CustomFilters.plist file present at the time of
# plugin installation (to avoid permanent elimination of
# custom filters that user created before plugin use)
try:
    if not os.path.isfile(FLM_BACKUP_ORIGINAL_FILE) and os.path.isfile(GLYPHS_PLIST_FILE):
        if not os.path.isdir(FLM_BACKUP_DIR):
            os.makedirs(FLM_BACKUP_DIR)
        shutil.copy(GLYPHS_PLIST_FILE, FLM_BACKUP_ORIGINAL_FILE)
except:
    pass

class FilterListManager(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.update_name = Glyphs.localize(
            {
                "en": "Update Filter Lists",
                "de": "Filterlisten aktualisieren"
            }
        )
        self.restoredefault_name = Glyphs.localize(
            {
                "en": "Restore Default Filter Lists",
                "de": "Standard-Filterlisten wiederherstellen",
            }
        )
        self.opendir_name = Glyphs.localize(
            {
                "en": "Open GlyphsFilters Directory",
                "de": "Verzeichnis GlyphsFilters öffnen",
            }
        )

    @objc.python_method
    def start(self):
        try:
            # new API in Glyphs 2.3.1-910
            new_update_menu_item = NSMenuItem(self.update_name, self.updateFilters_)
            new_restore_menu_item = NSMenuItem(self.restoredefault_name, self.restoreFilters_)
            new_opendir_menu_item = NSMenuItem(self.opendir_name, self.openGlyphsfiltersDirectory_)
            Glyphs.menu[EDIT_MENU].append(new_update_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_restore_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_opendir_menu_item)
        except Exception:
            main_menu = Glyphs.mainMenu()
            update_selector = objc.selector(self.updateFilters_, signature="v@:@")
            restore_selector = objc.selector(self.restoreFilters_, signature="v@:@")
            open_selector = objc.selector(
                self.openGlyphsfiltersDirectory_, signature="v@:@"
            )
            new_update_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                self.update_name, update_selector, ""
            )
            new_restore_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                self.restore_name, restore_selector, ""
            )
            new_open_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                self.opendir_name, open_selector, ""
            )
            new_update_menu_item.setTarget_(self)
            main_menu.itemWithTag_(5).submenu().addItem_(new_update_menu_item)
            new_restore_menu_item.setTarget_(self)
            main_menu.itemWithTag_(5).submenu().addItem_(new_restore_menu_item)
            new_open_menu_item.setTarget_(self)
            main_menu.itemWithTag_(5).submenu().addItem_(new_open_menu_item)

    def updateFilters_(self, sender):
        """Perform the list filter update"""
        # Expected filter definitions directory test
        if not self.filter_directory_is_present():
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to locate ~/GlyphsFilters directory! See log.",
            )
            logging.error(
                "Unable to locate the ~/GlyphsFilters directory.  This directory is mandatory for execution.  Please create it!"
            )
            return 0

        # --------------------------------------------
        #
        #  Backup original CustomFilters.plist file
        #
        # --------------------------------------------

        # read previous CustomFilters.plist definition file
        #  - used to prepare backup
        #  - used to define new definition file
        try:
            previous_plist_data = plistlib.readPlist(GLYPHS_PLIST_FILE)
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to read CustomFilters.plist file. See log.",
            )
            logging.error(
                "Unable to read the original CustomFilters.plist file in order to create a backup.  Error: "
                + str(e)
            )
            return 1

        new_plist_list = []  # storage data structure for new plist file definitions

        # backup the existing CustomFilters.plist file in the
        # ~/GlyphsFilters/backup directory
        try:
            if os.path.exists(FLM_BACKUP_DIR):
                shutil.move(GLYPHS_PLIST_FILE, FLM_BACKUP_PREVIOUS_FILE)
            else:
                os.makedirs(FLM_BACKUP_DIR)
                shutil.move(GLYPHS_PLIST_FILE, FLM_BACKUP_PREVIOUS_FILE)
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to backup your CustomFilters.plist file. See log.",
            )
            logging.error(
                "Unable to backup your CustomFilters.plist file. Error: " + str(e)
            )
            return 1

        # -----------------------------------------------------
        #
        #  Update CustomFilters.plist file with new definitions
        #
        # -----------------------------------------------------

        # parse local filter list definition files
        try:
            local_filter_definitions_list = self.get_local_filter_definitions_list()
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "Failed to parse local definition files. See log.",
            )
            logging.error("Failed to parse local definitions files.  Error: " + str(e))
            return 1

        # parse remote filter list definition files
        try:
            remote_filter_definitions_list = self.get_remote_filter_definitions_list()
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "Failed to parse remote definition files. See log.",
            )
            logging.error("Failed to parse remote definitions files.  Error: " + str(e))
            return 1

        plist_filter_definitions_list = []

        # create list with data structure that is formatted
        # so that it can be translated to a plist file on write
        for local_filter in local_filter_definitions_list:
            filter_dict = {}
            filter_dict["name"] = local_filter.name
            filter_dict["list"] = local_filter.list
            plist_filter_definitions_list.append(filter_dict)
            logging.info(
                "Found local definition file for the filter '" + local_filter.name + "'"
            )

        for remote_filter in remote_filter_definitions_list:
            filter_dict = {}
            filter_dict["name"] = remote_filter.name
            filter_dict["list"] = remote_filter.list
            plist_filter_definitions_list.append(filter_dict)
            logging.info(
                "Found remote definition file for the filter '"
                + remote_filter.name
                + "'"
            )

        # confirm that at least one definition was parsed from the definition files
        # if not, abort
        if (
            len(local_filter_definitions_list) == 0
            and len(remote_filter_definitions_list) == 0
        ):
            Glyphs.showNotification(
                "Filter List Manager",
                "Unable to identify new filter list definition files. No changes were made.",
            )
            logging.info(
                "Unable to identify new filter list definition files. There were no changes made to the filter list definitions."
            )
            return 0

        # filter out previous filter list contents in the CustomFilter.plist
        # file and keep previous non-filter list contents
        for previous_definition in previous_plist_data:
            if "list" in previous_definition:
                if "name" in previous_definition:
                    logging.info(
                        "Removing previously defined filter list '"
                        + previous_definition["name"]
                        + "'"
                    )
            else:
                new_plist_list.append(previous_definition)
                if "name" in previous_definition:
                    logging.info(
                        "Saving previously defined CustomFilters.plist data with name '"
                        + previous_definition["name"]
                        + "'"
                    )

        # add new data that was read from local and remote
        # definition files to a data format that translates
        # to a plist file
        for new_definition in plist_filter_definitions_list:
            new_plist_list.append(new_definition)
            if "name" in new_definition:
                logging.info("Adding new filter list '" + new_definition["name"] + "'")

        # write new CustomFilters.plist definition file to disk
        try:
            plistlib.writePlist(new_plist_list, GLYPHS_PLIST_FILE)
            logging.info("The new CustomFilter.plist file write was successful.")
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to write CustomFilters.plist file. See log.",
            )
            logging.error(
                "Unable to write new CustomFilters.plist file to disk. Error: " + str(e)
            )
            return 1

        Glyphs.showNotification(
            "Filter List Manager",
            "The filter list updates were successful.  Please quit and restart Glyphs.",
        )
        logging.info(
            "The filter list updates were successful.  Please quit and restart the Glyphs application to view the new filter lists."
        )

    def restoreFilters_(self, sender):
        """Perform restore of default list filters"""
        # copy the default definitions to the Glyphs application
        try:
            default_filters = plistlib.readPlist(FLM_DEFAULT_PLIST)
            plistlib.writePlist(default_filters, GLYPHS_PLIST_FILE)
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to restore the default filter list definitions. See log.",
            )
            logging.error(
                "Unable to restore default filter list definitions.  Error: " + str(e)
            )
            return 1

        Glyphs.showNotification(
            "Filter List Manager",
            "The default filter list restoration was successful.  Please quit and restart Glyphs.",
        )
        logging.info(
            "The default filter list restoration was successful.  Please quit and restart the Glyphs application to view the filter lists."
        )

    def openGlyphsfiltersDirectory_(self, sender):
        """Called from a plugin Edit menu item and opens the ~/GlyphsFilters directory in the macOS Finder"""
        if not os.path.isdir(FLM_GLYPHSFILTERS_DIR):
            Glyphs.showNotification(
                "Filter List Manager",
                "Unable to find ~/GlyphsFilters directory. Please create this path.",
            )
            logging.error(
                "Unable to find the ~/GlyphsFilters directory.  Please create this directory path."
            )
        else:
            subprocess.call(["open", FLM_GLYPHSFILTERS_DIR])
            logging.info(
                "The ~/GlyphsFilters directory was opened with the Edit menu item."
            )

    @objc.python_method
    def filter_directory_is_present(self):
        """Tests for presence of the ~/GlyphsFilters directory"""
        if not os.path.isdir(FLM_GLYPHSFILTERS_DIR):
            return False
        else:
            return True

    @objc.python_method
    def get_local_filter_definitions_list(self):
        """Reads and launches parsing of local definition files, returns a Python list of
           Filter objects that are created from the parse"""
        local_definitions_list = []

        if not os.path.isdir(FLM_GLYPHSFILTERS_DIR):
            # return an empty list if the directory is not found
            return []

        raw_definitions_file_list = [
            f
            for f in os.listdir(FLM_GLYPHSFILTERS_DIR)
            if os.path.isfile(os.path.join(FLM_GLYPHSFILTERS_DIR, f))
        ]
        definitions_file_list = []
        # filter list for dotfiles.  This eliminates macOS .DS_Store files that lead to errors during processing
        for definition_file in raw_definitions_file_list:
            if definition_file[0] == ".":
                pass
            else:
                definitions_file_list.append(definition_file)
        for definition_file in definitions_file_list:
            definition_path_list = definition_file.split(".")
            # define the filter list name as the file name
            new_filter = Filter(definition_path_list[0])
            with open(os.path.join(FLM_GLYPHSFILTERS_DIR, definition_file)) as f:
                # define the filter object with the definitions in the text data
                text = f.read()
                new_filter.define_list_with_newline_delimited_text(text)

            local_definitions_list.append(new_filter)

        return local_definitions_list

    @objc.python_method
    def get_remote_filter_definitions_list(self):
        """Pulls, reads, and launches parsing of remote definition files, returns a Python list of
           Filter objects that are created from the parse"""
        remote_definitions_list = []

        if not os.path.isfile(FLM_REMOTE_DEF_FILE):
            return []

        with open(FLM_REMOTE_DEF_FILE) as f:
            for line in f:
                url = line.strip()
                if len(url) == 0:
                    pass
                elif url[0] in ("#", "/"):
                    pass
                else:
                    # unquote URL defined in list to define file name
                    # (in case the user pasted a urlencoded string)
                    decoded_url = urllibparse.unquote(url)
                    parsed_url = urllibparse.urlparse(decoded_url).path
                    parsed_path = os.path.split(parsed_url)
                    filter_defintion_filename = parsed_path[1]
                    new_filter = Filter(filter_defintion_filename)

                    # quote URL defined in list to make HTTP GET request
                    response = urllibrequest.urlopen(url)
                    text = response.read()
                    new_filter.define_list_with_newline_delimited_text(text)
                    remote_definitions_list.append(new_filter)

        return remote_definitions_list

    @objc.python_method
    def __file__(self):
        """Glyphs plugin API specific method. Please leave this method unchanged"""
        return __file__


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
