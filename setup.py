from distutils.core import setup
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files_1 = package_files('dashboard/static/')
extra_files_2 = package_files('dashboard/views/')

extra_files = extra_files_1 + extra_files_2

setup(
    name='Dashboardpy',
    version='0.0.5',
    packages=['dashboard'],
    package_data={'dashboard': extra_files},
    url='https://github.com/isman7/Dashboardpy',
    license='MIT',
    author='Ismael Benito',
    author_email='isman7@gmail.com',
    description='Dashboardpy is an Bottlepy-based dashboard for Python!'
)
