from setuptools import setup, find_packages

with open('README.md') as f:
        long_description = f.read()

setup(
        name = "LEAM",
        version = '0.1.0',
        author = "LameStation",
        author_email = "contact@lamestation.com",
        description = "Play LameStation games on your desktop!",
        long_description = long_description,
        license = "GPLv3",
        url = "https://github.com/lamestation/LEAM",
        keywords = "emulator game converter lamestation desktop python spin",
        entry_points = {
            'console_scripts': [
                'leam = LEAM.__main__:cli'
            ]
        },
        packages=find_packages(),
        include_package_data=True,
        classifiers=[
            "Environment :: Console",
            "Development Status :: 1 - Planning",
            "Topic :: Games/Entertainment",
            "Topic :: System :: Emulators",
            "Topic :: Software Development :: Pre-processors",
            "Topic :: Multimedia :: Graphics :: Viewers",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 2 :: Only",
            "Programming Language :: Python :: 2.7",
            ]
        )
