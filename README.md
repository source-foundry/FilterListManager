# Filter List Manager (FLM)

## About

Filter List Manager (FLM) is a plugin for the [Glyphs font editor](https://glyphsapp.com) that automates the creation of glyph filter lists with simple newline-delimited glyph definition text files.  Definition files can be stored locally on your computer or remotely (e.g., in a Github repository) and used with the plugin.

## Plugin Installation

1. Download the [latest release archive](https://github.com/source-foundry/FilterListManager/releases) from the FLM repository Releases
2. Unpack the downloaded archive file
3. Open the unpacked directory
4. Double-click the plugin `FilterListManager.glyphsPlugin` in the top level of the directory to open it with the Glyphs application
5. Acknowledge that you want to install FLM in the Glyphs Install Plugin dialog that appears

### Upgrades

The `Preferences > Addons > Plugins` window in Glyphs will indicate when an update is available for the FLM plugin.  To upgrade your installed plugin, locate the [latest release of the plugin](https://github.com/source-foundry/FilterListManager/releases/latest) in the Github Releases and follow the same instructions that you followed for initial installation above.  

Changes that were included in the release are indicated in the repository [CHANGELOG.md](CHANGELOG.md).

## How to Make a Filter List Definition File

The filter list definition file is a newline-delimited text file that lists your desired glyph names.  See [DEFINITIONS.md](DEFINITIONS.md) for detailed documentation.

## Filter List Definition File Location

The filter list definition files that you use to define new filter lists can be stored on your local computer system or on a remote server that is accessible through HTTP GET requests.  Local and remote filter list definition files can be used simultaneously to define all desired Glyphs filter lists with the FLM plugin.

### Local definition files

Place the filter list definition files that you make in the top level of the directory `~/GlyphsFilters` on your macOS system.  If this directory does not exist after you install the FLM plugin, open your terminal and enter the following command:

```
$ mkdir ~/GlyphsFilters
```

The GlyphsFilters directory can be opened by selecting the Edit > Open GlyphsFilters Directory menu item in the Glyphs application after you install the FLM plugin.

### Remote definition files

You can upload filter list definition files to any publicly accessible web server or use files that have been shared by others with this approach.  You must create one additional settings file in the `~/GlyphsFilters` directory to define one or more URL where the FLM plugin can locate the remotely stored definition files.  

Save a text file on the path `~/GlyphsFilters/remote/defs.txt` with a newline-delimited list of URL that point to one or more filter list definition files.  Each URL represents a new filter list definition for the Glyphs application.  You may use the comment line indicators `#` and `//` in the `~/GlyphsFilters/remote/defs.txt` file.  Empty lines are also permitted (and ignored).

An example of a valid `~/GlyphsFilters/remote/defs.txt` file that points to two filter list definition files located on a remote Github server follows:

```
// Remote filter list definitions

# Mac Roman filter list definitions
https://raw.githubusercontent.com/source-foundry/charset-filters/master/Mac-Roman.txt

# MES-1 filter list definitions
https://raw.githubusercontent.com/source-foundry/charset-filters/master/MES-1.txt
```  

Please note in the above example that you must use the URL for the "Raw" text file if you push your definition files to Github.  This is formatted as `https://raw.githubusercontent.com/[account]/[project name]/[branch]/[filename]`. When you enter this URL in your browser you should see only the text file with no Github website UI around it.  If you see the Github UI in the browser window, the URL that you are viewing points to HTML text and this will lead to errors during the FLM plugin update attempt.

