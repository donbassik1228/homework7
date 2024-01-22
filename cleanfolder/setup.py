from setuptools import setup, find_packages

setup(
    name = 'cleanfolder',
    version = '0.0.1',
    entry_points = {
        'console_scripts':['clean-folder = cleanfolder.clean:main']
    },
    packages = find_packages()
) 