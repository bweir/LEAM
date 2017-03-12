import os
import sys
sys.path.insert(0, os.path.abspath('lib'))

from setuptools import setup, find_packages

with open('README.md') as f:
        long_description = f.read()

setup(
        name = "lamemaker",
        version = '0.1.0',
        author = "LameStation",
        author_email = "contact@lamestation.com",
        description = "Play LameStation games on your desktop!",
        long_description = long_description,
        license = "GPLv3",
        url = "https://github.com/lamestation/lamemaker",
        keywords = "emulator game converter lamestation desktop python spin",
        entry_points = {
            'console_scripts': [
                'lamemaker = lamemaker.__main__:cli'
            ]
        },
        package_dir={'':'lib'},
        packages=find_packages('lib'),
        include_package_data=True,
        classifiers=[
            "Environment :: Console",
            "Development Status :: 2 - Pre-Alpha",
            "Topic :: Games/Entertainment",
            "Topic :: System :: Emulators",
            "Topic :: Software Development :: Pre-processors",
            "Topic :: Multimedia :: Graphics :: Viewers",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3 :: Only",
            ]
        )
