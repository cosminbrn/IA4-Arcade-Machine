from setuptools import setup, find_packages
setup(
    name="interface",
    version="0.1",
    packages = find_packages(),
    package_dir={"": "."},
    install_requires=[
        "pygame"
    ],
    entry_points={
        'console_scripts': [
            'interface = interface.main:run'
        ]
    }
)