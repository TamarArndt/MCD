import sys
import os
import __main__


class FileHelper(object):
    """This class helps to do operations on filesystem level, for instance, searching files, getting path names etc.
    """
    def __init__(self):
        pass

    def get_project_cwd(self) -> str:
        """Intelligent method to detect the actual project working directory.

        :return: Full path to the project directory that contains the source code.
        :rtype: str
        """
        # take some pathes into account
        path_list = [sys.argv[0], os.path.dirname(os.path.realpath(sys.argv[0])), __main__.__file__, os.getcwd()]
        # get the project name
        project_name = self.get_project_dir_name()

        # find candidates (where project_name is part of the path)
        matching = [s for s in path_list if project_name in s and '.py' not in s]

        # the shortest path it is!
        project_cwd = max(matching, key=len)

        return project_cwd

    def get_project_dir_name(self) -> str:
        """Retrieves the name of the project directory (name of root directory where the *source code* (not the
        project directory one level higher) resides.

        :return: Only the name of the project, that is equivalent to the name of the *source code* directory.
        :rtype: str
        """
        project_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__ )), '..'))
        project_name = project_dir.split('/')[-1]

        return str(project_name)

