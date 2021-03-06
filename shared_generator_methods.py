# Get the current working directory OR user provided path
import os
import sys

import errno

from jinja2 import Template


def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            os.chmod(dir, mode)
        for file in files:
            os.chmod(file, mode)


# check if this directory exists, if not, create it
def check_directory(path):
    try:
        os.mkdir(path)
        change_permissions_recursive(path, 777)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            pass


def cwd():
    if len(sys.argv) >= 3:
        if sys.argv[2] == "--existing":
            return os.getcwd()
        else:
            return sys.argv[2]
    else:
        return os.getcwd()


def uppercase_first_letter(s):
    return s[0].upper() + s[1:]


def lowercase_first_letter(s):
    return s[0].lower() + s[1:]


def uppercase_views(views):
    return [uppercase_first_letter(view) for view in views]


def lower_module_names(modules):
    return [lowercase_first_letter(module.name) for module in modules]


def upper_module_names(modules):
    return [uppercase_first_letter(module.name) for module in modules]


# create all required directories for project
def create_directories(platform, modules):
    current_dir = cwd()
    check_directory(current_dir)

    if platform == "ios":
        check_directory("{}/Modules".format(current_dir))
        check_directory("{}/Common".format(current_dir))
        check_directory("{}/Common/Models".format(current_dir))

    for module in modules:
        check_directory("{}/{}".format(current_dir, lowercase_first_letter(module.name)))
        if platform == "ios":
            check_directory("{}/Modules/{}".format(current_dir, uppercase_first_letter(module.name)))
            check_directory("{}/Modules/{}/ViewControllers".format(current_dir, uppercase_first_letter(module.name)))
        else:
            check_directory("{}/{}/layouts".format(current_dir, uppercase_first_letter(module.name)))


def create_generic_file(directory, file_name, template):
    file_path = "{}/{}".format(directory, file_name)
    with open(file_path, 'w+') as generic_file:
        generic_file.write(Template(template).render())
