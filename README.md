# Wordpress Plugins Downloader

### Little helper tool for the [Wordfence Intelligence Bug Bounty Program](https://www.wordfence.com/threat-intel/bug-bounty-program/).

**Intendended use:** Download any number of plugins with any number of minimum installations. You can then use any SAST locally for an initial triage on the downloaded plugins.

## Installation
```
python3 -m venv venv
Activate virtual environment: source venv/bin/activate
Install requirements: pip3 install -r requirements
```

## Usage
1) `python3 main.py`
2) Just follow the prompts.

## App Behavior
- The plugins are downloaded to a "plugins" folder at the root of the project.
- The application skips previously downloaded plugins. E.g. if you download 2 plugins with at least 10000 downloads and decide to run the application again with the same conditions you will download other 2 plugins.
- In case you want to apply some regexes to the plugins in runtime, and wish to always delete the "plugins" folder at the end, you can pass `True` as the last argument to the method "download_plugins" in the main_py folder.
