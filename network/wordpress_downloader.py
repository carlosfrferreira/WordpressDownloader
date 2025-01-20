import io
import os
import shutil
import zipfile

import requests

from common.constants import Constants


class WordpressDownloader:
    """
    Module capable of downloading WordPress plugins.
    """
    BASE_URL = "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&browse=popular&request[" \
               "per_page]=50&request[page]="
    PLUGINS_FOLDER = "plugins/"

    # default constructor
    def __init__(self):
        self.max_pages = 0
        self.page = 1
        self.downloaded_plugins = 0

    def download_plugins(self, min_installations, number_of_plugins, dir_cleanup):
        """
        Downloads WordPress plugins to the local file system.

        :param min_installations: the minimum number of installations.
        :param number_of_plugins: the number of plugins to download.
        :param dir_cleanup: true if the plugins folder should be deleted at the end or false otherwise.
        """

        # Making a get request
        response = requests.get(self.BASE_URL + str(self.page))
        json_result = response.json()

        # number of pages
        if self.max_pages == 0:
            self.max_pages = json_result["info"]["pages"]

        print("page: " + str(self.page) + " of " + str(self.max_pages))
        print(Constants.LINE_SEPARATOR)

        # list of plugins
        plugins = json_result['plugins']
        for plugin in plugins:
            if plugin["active_installs"] >= min_installations:
                slug = plugin["slug"]
                if self._was_plugin_downloaded(slug):
                    print("skipping plugin " + slug + " since it was already downloaded.")
                    continue
                # if ("form" or "Form") not in plugin["short_description"]:
                #     continue
                self._download_plugin(plugin["download_link"])
                self.downloaded_plugins += 1
                print("plugin downloaded successfully")
                print("downloaded plugins: " + str(self.downloaded_plugins))
                print(Constants.LINE_SEPARATOR)
            else:
                print(
                    "skipping plugin " + plugin["slug"] + " with version " + plugin["version"] + " due to only " + str(
                        plugin["active_installs"]) + " installs.")
                self._handle_dir_cleanup(dir_cleanup)
                return True

            if self.downloaded_plugins == number_of_plugins:
                break
        if self.downloaded_plugins < number_of_plugins:
            self.page += 1
            return self.download_plugins(min_installations, number_of_plugins, dir_cleanup)
        else:
            print("downloaded plugins: " + str(self.downloaded_plugins))
            self._handle_dir_cleanup(dir_cleanup)
            return True

    def _handle_dir_cleanup(self, should_clean):
        """
        Deletes the downloaded WordPress plugins if the tool is configured to do so.
        :param should_clean: true if the directory should be deleted and false otherwise
        """

        if should_clean:
            print("deleting plugins folder...")
            shutil.rmtree(self.PLUGINS_FOLDER)
            print("current directory clean")
        else:
            print("current directory not cleaned")

    def _download_plugin(self, url):
        """
        Download a zip file from a WordPress plugin and extract it to the local file system.

        :param url: the url of the plugin to download.
        """

        print("downloading plugin: " + url)

        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(self.PLUGINS_FOLDER)

    def _was_plugin_downloaded(self, folder_name):
        """
        Checks if a plugin was already downloaded to the file system by its folder name.

        :param folder_name: the folder name of the plugin after extraction.
        :return: true if the plugin was already downloaded and false otherwise.
        """

        return os.path.isdir(self.PLUGINS_FOLDER + "/" + folder_name)
