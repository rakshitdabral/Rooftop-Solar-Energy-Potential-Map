from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT = "-e ."
def get_requirements(file_path:str)->List[str]:
    '''
        This Function will return all the required packages
    '''

    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name="solarmap-generation",
    version = "0.0.1",
    author="RakshitDabral",
    author_email="rakshitdabral1@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)