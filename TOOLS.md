## Filter List Management Tools

The filter list management tools include Python 3 scripts that are located in the [`tools` directory](https://github.com/source-foundry/FilterListManager/tree/master/tools) of the FLM repository.

If a Python 3 interpreter is not available on your system, please see the Python documentation at https://www.python.org/downloads/ for installation instructions.

The tools include:

### `exportfilters.py`

The `exportfilters.py` script exports existing Glyphs application filter lists to the FLM definition file format and saves these definition files in the GlyphsFilters directory.

#### Usage

Download the script file from the FLM repository and execute it from any directory on your macOS system with the following command in your terminal:

```
$ python3 exportfilters.py
```

Confirm that the files were exported to your GlyphsFilters directory and that the files include the expected glyph names.


### `glformatter.py`

The `glformatter.py` script formats lists of glyph names with additional Unicode data in a comment line above the glyph name definition.

The data that are added depend upon how you specify your glyph name in the definition file.  The possible data include:

- Unicode code point in hexadecimal format
- AGL-like nice name (if production name is specified in the file)
- Unicode code point hexadecimal format production name (if nice name is specified in the file)
- Unicode description of the code point

#### Usage

Download the script file from the FLM repository and execute it from any directory on your macOS system.  Include one or more file paths to local definition files as arguments to the script:

```
$ python3 glformatter.py [filepath 1] [filepath ...]
```

The script reformats the file in place and saves a backup of the in-file on the path `[filepath].pre`.


### `glinter.py`

The `glinter.py` script tests each glyph name that is specified in one or more filter list definition files against those that are defined in the Glyphs application GlyphData.xml file and the guidelines provided in the [Adobe OpenType Feature File Specification](https://github.com/adobe-type-tools/afdko/blob/develop/docs/OpenTypeFeatureFileSpecification.html) for *development* glyph names.  

The Glyphs application specific GlyphData.xml tests include any modifications that you've made to the GlyphData.xml data to define new glyph names.  The intent is to permit you to confirm that the glyph names that you specified in your definition list will be properly recognized and imported into the Glyphs application for use.

The GlyphData.xml tests that are performed include:

1) specified glyph name is a Glyphs application nice name
2) specified glyph name is a Glyphs application production name
3) specified glyph name is a Glyphs application alternate name

The glyph name passes if criteria for (1) or (2) are met.  The script suggests conversion to the nice name or production name (with those values!) if criteria for (3) are met.  If there is no match for (1), (2), and (3), the script raises an error and indicates the glyph name and file path to the definition file.

The Adobe OpenType Feature File Specification tests that are performed include:

1) glyph name is 63 characters or less in length
2) glyph name does not start with a period (except ".null" and ".notdef")
3) glyph name only includes characters in the set:
    - `A-Z`
    - `a-z`
    - `0-9`
    - `.` (period)
    - `_` (underscore)
    - `*` (asterisk)
    - `+` (plus sign)
    - `-` (hyphen)
    - `:` (colon)
    - `^` (circumflex accent)
    - `|` (vertical bar)
    - `~` (tilde)
    
#### Usage

Download the script file from the FLM repository and execute it from any directory on your macOS system.  Include one or more file paths to local definition files as arguments to the script:

```
$ python3 glinter.py [filepath 1] [filepath ...]
```

Please note that the script does not modify the filter list definition file during execution.  It indicates potential errors for your review. You must edit the file to address valid errors.