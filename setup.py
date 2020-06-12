import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = ['numpy==1.17.0', 'pandas==0.25.3', 'scipy==1.3.0',
                'tqdm==4.28.1', 'matplotlib==3.1.1', 'shapely==1.6.4', 'geopy=1.13.0']

setuptools.setup(
    name="CityToolkit", # Replace with your own username
    version="0.0.1",
    # packages=['ctool', 'ctool.spatialunit', 'ctool.gis', 'ctool.preprocess', 'ctool.visualization'],
    author="YY",
    description="Toolkit for smartcity related works",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)