import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='pybgpkit',
    version='0.2.1',
    description='BGPKIT tools Python bindings',
    url='https://github.com/bgpkit/pybgpkit',
    author='Mingwei Zhang',
    author_email='mingwei@bgpkit.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        # available on pip
        'dataclasses_json',
        'pybgpkit-parser==0.2.1',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            "pybgpkit=bgpkit.cli:main"
        ]
    }
)
