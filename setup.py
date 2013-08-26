from setuptools import setup, find_packages

setup(
    name='corsa',
    version="0.1.1",
    description='CORS proxy and web server for static apps',
    author='Oliver Tonnhofer',
    author_email='olt@bogosoft.com',
    url='https://github.com/olt/corsa',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'corsa = corsa.app:main',
        ],
    },
    install_requires=[
        'tornado',
    ],
)
