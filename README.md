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

The filter list definition file is a newline-delimited text file that lists your desired glyph names.  See [DEFINITIONS.md](DEFINITIONS.md) for detailed documentation.

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
