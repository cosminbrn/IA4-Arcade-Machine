from setuptools import setup, find_packages
setup(
    name="rouge_tetris",
    version="0.1",
    packages = find_packages(),
    package_dir={"": "."},
    install_requires=[
        "pygame"
    ],
    entry_points={
        'console_scripts': [
            'rouge_tetris = rouge_tetris.main:run'
        ]
    }
)