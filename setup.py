from setuptools import setup, find_packages

setup(
    name='Corsa',
    version="0.1.0",
    description='CORS proxy and web server for static apps',
    author='Oliver Tonnhofer',
    author_email='olt@bogosoft.com',
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
