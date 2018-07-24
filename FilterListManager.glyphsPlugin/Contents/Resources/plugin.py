# encoding: utf-8

# ##########################################################################################################
#
#
#   Filter List Manager
#   Copyright 2018 Christopher Simpkins
#   Apache License 2.0
#
#
# ##########################################################################################################

import objc
import os
import plistlib
import sys

from GlyphsApp import *
from GlyphsApp.plugins import *


class FilterListManager(GeneralPlugin):
    def settings(self):
        # TODO: modify localized versions of strings
        self.update_name = Glyphs.localize({'en': u'Update Filter Lists', 'de': u'XXXX'})
        self.restoredefault_name = Glyphs.localize({'en': u'Restore Default Filter Lists', 'de': u'XXXX'})

    def start(self):
        try:
            # new API in Glyphs 2.3.1-910
            new_update_menu_item = NSMenuItem(self.update_name, self.update_filters)
            new_restore_menu_item = NSMenuItem(self.restoredefault_name, self.restore_filters)
            Glyphs.menu[EDIT_MENU].append(new_update_menu_item)
            Glyphs.menu[EDIT_MENU].append(new_restore_menu_item)
        except Exception:
            main_menu = Glyphs.mainMenu()
            update_selector = objc.selector(self.update_filters, signature='v@:@')
            restore_selector = objc.selector(self.restore_filters, signature='v@:@')
            new_update_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.update_name, update_selector, "")
            new_restore_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.restore_name, restore_selector, "")
            new_update_menu_item.setTarget_(self)
            main_menu.itemWithTag_(5).submenu().addItem_(new_update_menu_item)
            new_restore_menu_item.setTarget_(self)
            main_menu.itemWithTag_(5).submenu().addItem_(new_restore_menu_item)

    def update_filters(self, sender):
        """Perform the list filter update"""
        # test to confirm that the expected update directory is present
        if not self.filter_directory_is_present():
            Glyphs.showNotification('Filter List Manager', 'ERROR: Unable to locate GlyphsFilter directory!')
        else:
            # BEGIN UPDATE
            pass
            # TODO

            Glyphs.showNotification('Filter List Manager', 'The filter list updates were successful.  Please quit and restart Glyphs.')

    def restore_filters(self, sender):
        """Perform restore of default list filters"""
        write_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Glyphs", "CustomFilter.plist")
        read_path = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Glyphs", "Plugins", "FilterListManager.glyphsPlugin", "Contents", "Resources", "CustomFilter.plist")
        default_filters = plistlib.readPlist(read_path)
        plistlib.writePlist(default_filters, write_path)
        Glyphs.showNotification('Filter List Manager', 'The default filter list restoration was successful.  Please quit and restart Glyphs.')

    def filter_directory_is_present(self):
        if not os.path.isdir(os.path.join(os.path.expanduser("~"), "GlyphsFilters")):
            return False
        else:
            return True

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
