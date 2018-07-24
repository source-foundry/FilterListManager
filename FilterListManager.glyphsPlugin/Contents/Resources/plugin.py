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

import objc
import os
import plistlib
import subprocess
import sys

from GlyphsApp import *
from GlyphsApp.plugins import *

# TODO: add logging of errors

class FilterListManager(GeneralPlugin):
    def settings(self):
        # TODO: modify localized versions of strings
        self.update_name = Glyphs.localize({'en': u'Update Filter Lists', 'de': u'XXXX'})
        self.restoredefault_name = Glyphs.localize({'en': u'Restore Default Filter Lists', 'de': u'XXXX'})
        self.opendir_name = Glyphs.localize({'en': u'Open GlyphsFilters Directory', 'de': u'XXXX'})

    def start(self):
        try:
            # new API in Glyphs 2.3.1-910
            new_update_menu_item = NSMenuItem(self.update_name, self.update_filters)
            new_restore_menu_item = NSMenuItem(self.restoredefault_name, self.restore_filters)
            new_opendir_menu_item = NSMenuItem(self.opendir_name, self.open_glyphsfilters_directory)
            Glyphs.menu[EDIT_MENU].append(new_update_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_restore_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_opendir_menu_item)
        except Exception:
            main_menu = Glyphs.mainMenu()
            update_selector = objc.selector(self.update_filters, signature='v@:@')
            restore_selector = objc.selector(self.restore_filters, signature='v@:@')
            open_selector = objc.selector(self.open_glyphsfilters_directory, signature='v@:@')
            new_update_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.update_name, update_selector, "")
            new_restore_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.restore_name, restore_selector, "")
            new_open_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.opendir_name, open_selector, "")
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
            Glyphs.showNotification('Filter List Manager', 'ERROR: Unable to locate GlyphsFilter directory!')
            return 0

        plist_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Glyphs", "CustomFilter.plist")
        previous_plist_data = plistlib.readPlist(plist_path)
        new_plist_list = []  # storage data structure for new plist file definitions

        # TODO: backup old plist file

        # Begin update
        local_filter_definitions_list = self.get_local_filter_definitions_list()
        # TODO: add support for remote filter files
        plist_filter_definitions_list = []

        # create list with plist formatted data
        for a_filter in local_filter_definitions_list:
            filter_dict = {}
            filter_dict["name"] = a_filter.name
            filter_dict["list"] = a_filter.list
            plist_filter_definitions_list.append(filter_dict)

        if len(local_filter_definitions_list) == 0:
            # TODO: modify this test when add support for remote files
            Glyphs.showNotification('Filter List Manager', 'Unable to identify new filter list definition files. No changes were made.')
            return 0

        for previous_definition in previous_plist_data:
            if "list" in previous_definition:
                pass
            else:
                new_plist_list.append(previous_definition)

        # add new data that was read from definition files to Python list
        for new_definition in plist_filter_definitions_list:
            new_plist_list.append(new_definition)

        plistlib.writePlist(new_plist_list, plist_path)

        Glyphs.showNotification('Filter List Manager', 'The filter list updates were successful.  Please quit and restart Glyphs.')

    def restore_filters(self, sender):
        """Perform restore of default list filters"""
        write_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Glyphs", "CustomFilter.plist")
        read_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Glyphs", "Plugins", "FilterListManager.glyphsPlugin", "Contents", "Resources", "CustomFilter.plist")
        default_filters = plistlib.readPlist(read_path)
        plistlib.writePlist(default_filters, write_path)
        Glyphs.showNotification('Filter List Manager', 'The default filter list restoration was successful.  Please quit and restart Glyphs.')

    def open_glyphsfilters_directory(self, sender):
        glyphs_filters_dirpath = os.path.join(os.path.expanduser("~"), "GlyphsFilters")
        if not os.path.isdir(glyphs_filters_dirpath):
            Glyphs.showNotification('Filter List Manager', 'Unable to find ~/GlyphsFilters directory. Please create this path.')
        else:
            subprocess.call(["open", glyphs_filters_dirpath])

    def filter_directory_is_present(self):
        if not os.path.isdir(os.path.join(os.path.expanduser("~"), "GlyphsFilters")):
            return False
        else:
            return True

    def get_local_filter_definitions_list(self):
        local_definitions_list = []
        filter_definition_dir_path = os.path.join(os.path.expanduser("~"), "GlyphsFilters")
        if not os.path.isdir(filter_definition_dir_path):
            # return an empty list if the directory is not found
            return []
        else:
            definitions_file_list = [f for f in os.listdir(filter_definition_dir_path) if
                                     os.path.isfile(os.path.join(filter_definition_dir_path, f))]
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

    def __file__(self):
        """Please leave this method unchanged"""
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
            elif test_item[0] in self.comment_delimiters:  # discard comment lines in definition file
                pass
            else:
                filtered_code_point_list.append(test_item)
        self.list = filtered_code_point_list
