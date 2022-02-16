from setuptools import setup, find_packages

setup(
    name='treehw1',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "astunparse>=1.6.3",
        "cycler>=0.11.0",
        "fonttools>=4.29.1",
        "kiwisolver>=1.3.2",
        'matplotlib>=3.5.1',
        "networkx==2.6.3",
        "numpy==1.22.1",
        "packaging==21.3",
        "Pillow==9.0.0",
        "pydot==1.4.2",
        "pyparsing==3.0.7",
        "python-dateutil==2.8.2",
        "six == 1.16.0",
        "urllib3 >= 1.26.8",
        "chardet >= 3.0.4"
    ],
)
