## Filter List Definition File Spec

The filter list definition file is a text file that is formatted with a newline-delimited list of glyph names to include in the new Glyphs filter list.  Each definition file defines a single filter list. You can use one or more filter list definition files simultaneously during updates with the FLM plugin and these settings files can be stored on your local macOS system or on a remote web server that is accessible through HTTP GET requests.

### Filter list name

Define the filter list name in the base name of the definition file.  You may include spaces, hyphens, and parentheses in these names.  

The following are examples of how filenames are mapped to filter list names in the Glyphs application user interface:

- `Esperanto.txt` = `Esperanto`
- `Basic Latin.txt` = `Basic Latin`
- `MES-1.txt` = `MES-1`
- `Serbian (Latin).txt` = `Serbian (Latin)`

The plugin provides support for empty lines in the body of the text file to improve readability and organization of the document.  Use as many empty lines as you need in the definition file to format it however it is most helpful for sharing and maintenance of the definitions.

### Glyph names

Format your filter list definition file with one glyph name per line.  This is called newline-delimited format.  Use either Unicode hexadecimal code point style names (e.g, `uni00F6`) or AGL-style nice names (e.g., `odieresis`) as supported by the Glyphs application.

### Comment line support

Comment lines (i.e., lines in the definition file that include text that is not intended for use as part of the glyph name list) are indicated with either `#` or `//` at the beginning of the line.  Include one of these two comment indicators at the beginning of each line that is intended to be a comment line in your definition file document.  It is not mandatory to use comment indicators on empty lines that are used to format your document (e.g., empty lines between glyph name definitions, see example below).

Note: Comment indicators can be added to the start of one or more lines that includes glyph names in order to exclude these lines from the list of glyphs used in a filter.  This can be helpful if you need to make periodic modifications to sets of glyph names in a given list.  Simply place a `#` or `//` at the start of the glyph name line to exclude it from the filter list definition.

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

The same definition file could be written in a much more concise format like this:

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

The filter list that is created in the Glyphs application does not differ between the two definition file examples above.  Use the approach that works best for you.
