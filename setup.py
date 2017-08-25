from setuptools import setup, find_packages
import os

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='jumpy-pig',
    version="0.0.1",
    description="A game for Lila",
    url="https://github.com/sminez/jumpy-pig",
    author="Innes Anderson-Morrison",
    author_email='innesdmorrison@gmail.com',
    install_requires=[
        'pygame==1.9.3',
        'pytmx==3.21.3'
    ],
    setup_requires=[],
    tests_require=[],
    extras_require={},
    packages=find_packages(),
    package_dir={'jumpy-pig': 'jumpy-pig'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta'
    ],
    include_package_data=True,
    package_data={
        '': [
            'assets/sounds/*.mp3',
            'assets/sounds/*.wav',
            'assets/sprites/*.png',
            'assets/sprites/jumpy/*.png',
            'levels/*.png',
            'levels/tmx-files/*.tmx',
            'levels/tmx-files/*.tsx',
        ],
    },
    entry_points={
        'console_scripts': [
            'jumpy = src.main:main',
        ]
    },
)
