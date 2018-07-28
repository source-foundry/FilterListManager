# Filter List Manager (FLM)

## About

Filter List Manager (FLM) is a plugin for the [Glyphs font editor](https://glyphsapp.com) that automates the creation of glyph filter lists with simple newline-delimited glyph definition text files.  Definition files can be stored locally on your computer or remotely (e.g., in a Github repository) and used with the plugin.

## Plugin Installation

1. Download the [latest release of the plugin](https://github.com/source-foundry/FilterListManager/releases) from our repository Releases
2. Unpack the downloaded repository archive
3. Open the unpacked directory
4. Double-click the plugin `FilterListManager.glyphsPlugin` to open it with the Glyphs application
5. Acknowledge that you want to install FLM in the Glyphs Install Plugin dialog that appears

### Upgrades

The `Preferences > Addons > Plugins` window in Glyphs will indicate when an update is available for the FLM plugin.  To upgrade your installed plugin, locate the [latest release of the plugin](https://github.com/source-foundry/FilterListManager/releases/latest) in the Github Releases and follow the same instructions that you followed for initial installation above.  

Changes that were included in the release are indicated in the repository [CHANGELOG.md](CHANGELOG.md).

## How to Make a Filter List Definition File

The filter list definition file is a text file that is formatted with a newline-delimited list of glyph names to include in the new Glyphs filter list.  Each definition file defines a single filter list. You can use one or more filter list definition files simultaneously during updates with the FLM plugin.

### Filter list name

Define the filter list name in the base name of the definition file.  You may include spaces, hyphens, and parentheses in these names.  

The following are examples of how filenames are mapped to filter list names in the Glyphs application user interface:

- `Esperanto.txt` = `Esperanto`
- `Basic Latin.txt` = `Basic Latin`
- `MES-1.txt` = `MES-1`
- `Serbian (Latin).txt` = `Serbian (Latin)`

The plugin provides support for empty lines to improve readability and organization of the document.  Use as many empty lines as you need in the definition file to format it however it is most helpful for sharing and maintenance of the definitions.

### Glyph names

Format your filter list definition file with one glyph name per line.  This is called newline-delimited format.  Use either Unicode hexadecimal code point style names (e.g, `uni00F6`) or AGL-style nice names (e.g., `odieresis`) as supported by the Glyphs application.

### Comment line support

Comment lines (i.e., lines in the definition file that are not intended to be used as part of the definition list) are indicated with either `#` or `//` at the beginning of the line.  Include one of these two comment indicators at the beginning of each line that is intended to be a comment line in your definition file document.

Note: Comment indicators can be added to the start of a line that includes a glyph name in order to filter these lines out of the final filter list.  This is called "commenting out" a glyph.

### Example

The following is an example of a valid filter list definition file that includes comment and empty line formatting:

##### Filename: `Esperanto.txt`

```
// -------------------------------------------------
// Esperanto Glyphs filter list definition file
// Copyright 2018, Some Person
// MIT License
// -------------------------------------------------

# U+0108
Ccircumflex

# U+0109
ccircumflex

# U+011C
Gcircumflex

# U+011D
gcircumflex

# U+0124
Hcircumflex

# U+0125
hcircumflex

# U+0134
Jcircumflex

# U+0135
jcircumflex

# U+015C
Scircumflex

# U+015D
scircumflex

# U+016C
Ubreve

# U+016D
ubreve

```

The same definition file could be specified in a much more concise format like this:

##### Filename: `Esperanto.txt`

```
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

The filter list that is created in the Glyphs application does not differ between the two definition files.  Use the approach that works best for you.

## Filter List Definition File Location

The filter list definition files can be stored on your local computer system or on a remote server that is accessible through HTTP GET requests.  The FLM plugin works with both file types.  Details about how to use each approach are below.

### Local definition files

Place the filter list definitions files that you make in the top level of the directory `~/GlyphsFilters` on your macOS system.  This directory can be opened after you install the FLM plugin by selecting the Edit > Open GlyphsFilters Directory menu item in the Glyphs application.  Local and remote filter list definition files can be used simultaneously to define all desired Glyphs filter lists with the FLM plugin  (see Remote definition files documentation below).

### Remote definition files

You can upload filter list definition files to any publicly accessible web server or use files that are pushed by others for shared use.  This approach requires one additional settings file in the `~/GlyphsFilters` directory that is used to define one or more URL where the FLM plugin can access the definition files.  

To use remote filter list definition files, a text file must be saved on the path `~/GlyphsFilters/remote/defs.txt` with a newline-delimited list of URL that point to one or more filter list definition files.  Each URL represents a new filter list definition for the Glyphs application.  You may use the comment line indicators `#` and `//` in the `~/GlyphsFilters/remote/defs.txt` file.  Empty lines are also permitted.

An example remote filter list definition file that points to two new filters located on a remote Github server follows:

```
// Remote filter list definitions

# Mac Roman filter list definitions
https://raw.githubusercontent.com/source-foundry/charset-filters/master/Mac-Roman.txt

# MES-1 filter list definitions
https://raw.githubusercontent.com/source-foundry/charset-filters/master/MES-1.txt
```  

Please note in the above example that you must use the URL for the "Raw" text file if you push your definition files to Github.  This is formatted as `https://raw.githubusercontent.com/[account]/[project name]/[branch]/[filename]`. When you enter this URL in your browser you should see only the text file with no Github website UI around it.  If you see the latter, you are pointing to a HTML text file and this will lead to errors during the FLM plugin update attempt.

Remote and local filter list definition files can be used simultaneously to define all desired Glyphs filter lists with the FLM plugin (see Local definition files documentation above for additional details).
