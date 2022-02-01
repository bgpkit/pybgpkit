import setuptools

setuptools.setup(
    name='pybgpkit',
    version='0.0.1',
    description='BGPKIT tools Python bindings',
    url='https://github.com/bgpkit/pybgpkit',
    author='Mingwei Zhang',
    author_email='mingwei@bgpkit.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        # available on pip
        'pybgpkit-parser==0.0.1',
    ],
    entry_points={'console_scripts': [
    ]}
)
