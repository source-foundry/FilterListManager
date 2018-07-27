# encoding: utf-8

# ##########################################################################################################
#
#
#   Filter List Manager
#   A plugin for the Glyphs font editor
#   Copyright 2018 Christopher Simpkins
#   Apache License 2.0
#
#
# ##########################################################################################################

import logging
import objc
import os
import plistlib
import shutil
import subprocess
import urllib2
import urlparse

from GlyphsApp import *
from GlyphsApp.plugins import *

# Logging setup
log_dir = os.path.join(os.path.expanduser("~"), "GlyphsFilters", "logs")
log_path = os.path.join(log_dir, "flm.log")
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    filename=log_path,
    filemode="w",
    format="%(asctime)s %(levelname)s  %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
)


class FilterListManager(GeneralPlugin):
    def settings(self):
        # TODO: modify localized versions of strings
        self.update_name = Glyphs.localize(
            {"en": u"Update Filter Lists", "de": u"XXXX"}
        )
        self.restoredefault_name = Glyphs.localize(
            {"en": u"Restore Default Filter Lists", "de": u"XXXX"}
        )
        self.opendir_name = Glyphs.localize(
            {"en": u"Open GlyphsFilters Directory", "de": u"XXXX"}
        )

    def start(self):
        try:
            # new API in Glyphs 2.3.1-910
            new_update_menu_item = NSMenuItem(self.update_name, self.update_filters)
            new_restore_menu_item = NSMenuItem(
                self.restoredefault_name, self.restore_filters
            )
            new_opendir_menu_item = NSMenuItem(
                self.opendir_name, self.open_glyphsfilters_directory
            )
            Glyphs.menu[EDIT_MENU].append(new_update_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_restore_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_opendir_menu_item)
        except Exception:
            main_menu = Glyphs.mainMenu()
            update_selector = objc.selector(self.update_filters, signature="v@:@")
            restore_selector = objc.selector(self.restore_filters, signature="v@:@")
            open_selector = objc.selector(
                self.open_glyphsfilters_directory, signature="v@:@"
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

    def update_filters(self, sender):
        """Perform the list filter update"""
        # Expected filter definitions directory test
        if not self.filter_directory_is_present():
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to locate GlyphsFilters directory!",
            )
            logging.error(
                "Unable to locate the ~/GlyphsFilters directory.  This directory is mandatory for execution.  Please create it!"
            )
            return 0

        # define the Glyphs CustomFilters.plist file path for reads/writes
        plist_path = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Glyphs",
            "CustomFilter.plist",
        )

        # --------------------------------------------
        #
        #  Backup original CustomFilters.plist file
        #
        # --------------------------------------------

        # read original CustomFilters.plist definition file
        #  - used to prepare backup
        #  - used to define new definition file
        try:
            previous_plist_data = plistlib.readPlist(plist_path)
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

        previous_plist_backup_dir = os.path.join(
            os.path.expanduser("~"), "GlyphsFilters", "backup"
        )
        previous_plist_backup_path = os.path.join(
            previous_plist_backup_dir, "CustomFilter.plist"
        )

        try:
            if os.path.exists(previous_plist_backup_dir):
                shutil.move(plist_path, previous_plist_backup_path)
            else:
                os.makedirs(previous_plist_backup_dir)
                shutil.move(plist_path, previous_plist_backup_path)
        except Exception as e:
            Glyphs.showNotification(
                "Filter List Manager",
                "ERROR: Unable to backup original CustomFilters.plist file. See log.",
            )
            logging.error(
                "Unable to backup original CustomFilters.plist file. Error: " + str(e)
            )
            return 1

        # -----------------------------------------------------
        #
        #  Update CustomFilters.plist file with new definitions
        #
        # -----------------------------------------------------

        local_filter_definitions_list = self.get_local_filter_definitions_list()
        remote_filter_definitions_list = self.get_remote_filter_definitions_list()
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

        # add new data that was read from local and remote
        # definition files to a data format that translates
        # to a plist file
        for new_definition in plist_filter_definitions_list:
            new_plist_list.append(new_definition)

        # write new CustomFilters.plist definition file to disk
        try:
            plistlib.writePlist(new_plist_list, plist_path)
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

    def restore_filters(self, sender):
        """Perform restore of default list filters"""
        # define the path to write out the default definitions file
        write_path = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Glyphs",
            "CustomFilter.plist",
        )
        # define the CustomFilters.plist file path that is embedded in the plugin
        # for restoration of the default filter lists in the Glyphs application
        read_path = os.path.join(
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
        # copy the default definitions to the Glyphs application
        try:
            default_filters = plistlib.readPlist(read_path)
            plistlib.writePlist(default_filters, write_path)
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

    def open_glyphsfilters_directory(self, sender):
        """Called from a plugin Edit menu item and opens the ~/GlyphsFilters directory in the macOS Finder"""
        glyphs_filters_dirpath = os.path.join(os.path.expanduser("~"), "GlyphsFilters")
        if not os.path.isdir(glyphs_filters_dirpath):
            Glyphs.showNotification(
                "Filter List Manager",
                "Unable to find ~/GlyphsFilters directory. Please create this path.",
            )
            logging.error(
                "Unable to find the ~/GlyphsFilters directory.  Please create this directory path."
            )
        else:
            subprocess.call(["open", glyphs_filters_dirpath])
            logging.info(
                "The ~/GlyphsFilters directory was opened with the Edit menu item."
            )

    def filter_directory_is_present(self):
        """Tests for presence of the ~/GlyphsFilters directory"""
        if not os.path.isdir(os.path.join(os.path.expanduser("~"), "GlyphsFilters")):
            return False
        else:
            return True

    def get_local_filter_definitions_list(self):
        """Reads and launches parsing of local definition files, returns a Python list of
           Filter objects that are created from the parse"""
        local_definitions_list = []
        filter_definition_dir_path = os.path.join(
            os.path.expanduser("~"), "GlyphsFilters"
        )
        if not os.path.isdir(filter_definition_dir_path):
            # return an empty list if the directory is not found
            return []

        raw_definitions_file_list = [
            f
            for f in os.listdir(filter_definition_dir_path)
            if os.path.isfile(os.path.join(filter_definition_dir_path, f))
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
            with open(os.path.join(filter_definition_dir_path, definition_file)) as f:
                # define the filter object with the definitions in the text data
                text = f.read()
                new_filter.define_list_with_newline_delimited_text(text)

            local_definitions_list.append(new_filter)

        return local_definitions_list

    def get_remote_filter_definitions_list(self):
        """Pulls, reads, and launches parsing of remote definition files, returns a Python list of
           Filter objects that are created from the parse"""
        remote_definitions_list = []
        remote_filter_definitions_path = os.path.join(
            os.path.expanduser("~"), "GlyphsFilters", "remote", "defs.txt"
        )
        if not os.path.isfile(remote_filter_definitions_path):
            return []

        with open(remote_filter_definitions_path) as f:
            for line in f:
                url = line.strip()
                if len(url) == 0:
                    pass
                elif url[0] in ("#", "/"):
                    pass
                else:
                    parsed_url = urlparse.urlparse(url).path
                    parsed_path = os.path.split(parsed_url)
                    filter_defintion_filename = parsed_path[1]
                    new_filter = Filter(filter_defintion_filename)
                    response = urllib2.urlopen(url)
                    text = response.read()
                    new_filter.define_list_with_newline_delimited_text(text)
                    remote_definitions_list.append(new_filter)

        return remote_definitions_list

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
