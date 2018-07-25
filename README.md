# Filter List Manager

Glyphs font editor filter list manager (FLM) plugin

## Status

Pre-release testing.  Not suitable for production use yet.

## Testers

**NOTE**: Please backup your `~/Libary/Application Support/Glyphs/CustomFilter.plist` file before you use this pre-release version of the plugin!

### Install
1. [Download the source code repository](https://github.com/source-foundry/FilterListManager/releases/latest)
2. Unpack the downloaded archive file
3. Double-click `FilterListManager.glyphsPlugin` in the root of the source directory
4. Accept the plugin install dialogs that are displayed in the Glyphs application

### Export Existing Glyphs Filter Lists for Use with the FLM Plugin

If you would like to export your existing Glyphs filter lists as definition files that work with this plugin, use the [exportfilters.py Python script](https://github.com/source-foundry/FilterListManager/blob/master/tools/exportfilters.py) located in the `tools` directory of this repository BEFORE YOU PERFORM THE FIRST UPDATE with the FLM plugin.  See Usage documentation in the header of the script for details.

### Tests

1) You should find three new menu items in the Edit menu:

    - Update Filter Lists
    - Restore Default Filter Lists
    - Open GlyphsFilters Directory
    
2) When you select Edit > Open GlyphsFilters Directory, you should receive a notification that this directory is missing.

3) Make the GlyphsFilters directory on the path `~/GlyphsFilters` with the command `mkdir ~/GlyphsFilters` in your terminal

4) When you select Edit > Open GlyphsFilters Directory in Glyphs, you should find that the GlyphsFilters directory now opens to an empty directory in your macOS Finder

5) Add one or more filter list definition files to the `~/GlyphsFilters` directory that are specified as follows:

    - define your filter list name using the filename (e.g. Esperanto.txt yields filter list 'Esperanto')
    - use a newline between each definition
    - use a `#` or `//` at the start of comment lines
    - you may include empty lines for formatting purposes, they should be ignored...
    
An example definition file that follows these specs is as follows:

```
// Esperanto filter list
// by Dapper Fellow

Ccircumflex
ccircumflex
Gcircumflex
gcircumflex
Hcircumflex
hcircumflex
Jcircumflex
jcircumflex
Scircumflex
scircumflex
Ubreve
ubreve

```


6) Select Edit > Update Filter Lists.  You should receive a notification that your filter list definition file was updated.  Close Glyphs and reopen.  Check your filter list name list on the left side of the editor window and confirm that all expected filter lists are there and contain the expected Unicode code points.

7) Select Edit > Restore Default Filter Lists.  Close Glyphs and reopen.  Check your filter list name list on the left side of the editor window and confirm that the Mac Roman, Windows 1252, and ASCII lists are there and contain the expected Unicode code points.

To return to the set of filter lists that you had before you used the FLM plugin, replace the file on the path `~/Libary/Application Support/Glyphs/CustomFilter.plist` with the backup file that you made before you started these tests. Quit and reopen Glyphs to view your restored default filter lists.  Uninstall the testing plugin by deleting the directory on the path `~/Libary/Application Support/Glyphs/Plugins/FilterListManager.glyphsPlugin`.

