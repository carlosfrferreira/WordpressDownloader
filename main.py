# This is the starting point of the program
from common.constants import Constants
from network.wordpress_downloader import WordpressDownloader


def ask_user(user_prompt):
    """
    Asks user for input.

    :param user_prompt: the prompt to show the user.
    :return: user input.
    """

    user_input = 0
    while user_input <= 0:
        try:
            user_input = int(input(user_prompt))
            if user_input <= 0:
                print(Constants.INPUT_ERROR_INTEGER)
        except ValueError:
            print(Constants.INPUT_ERROR_INTEGER)
    return user_input


if __name__ == '__main__':
    wordpress_downloader = WordpressDownloader()

    # ask the user for the minimum number of installations of the plugin
    minimum_no_installations = ask_user(Constants.INPUT_NUMBER_OF_INSTALLATIONS)

    # ask the user how many plugins to download
    no_plugins_to_download = ask_user(Constants.INPUT_NUMBER_OF_PLUGINS_TO_DOWNLOAD)

    wordpress_downloader.download_plugins(minimum_no_installations, no_plugins_to_download, False)
