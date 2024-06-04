import platform

class OSUtils:

    @classmethod
    def is_windows(cls):
        """! Verify if the operational system used is Windows
        @return True if it is Windows, False, otherwise.
        """

        return platform.system() == "Windows"

    @classmethod
    def is_mac(cls):
        return platform.system() == "Darwin"

    @classmethod
    def is_unix(cls):
        return platform.system() == "Linux"
