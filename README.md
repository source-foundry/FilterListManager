# Filter List Manager (FLM)

## About

Filter List Manager (FLM) is a plugin for the [Glyphs font editor](https://glyphsapp.com) that automates the creation of glyph filter lists with simple newline-delimited glyph definition text files.  Definition files can be stored locally on your computer or remotely (e.g., in a Github repository) and used with the plugin.

## Plugin Installation

1. Download the [latest release of the plugin](https://github.com/source-foundry/FilterListManager/releases) from our repository Releases
2. Unpack the downloaded repository archive
3. Open the unpacked directory
4. Double-click the plugin `FilterListManager.glyphsPlugin` to open it with the Glyphs application
5. Acknowledge that you want to install FLM in the Glyphs Install Plugin dialog that appears

## Filter List Definition File Specification

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