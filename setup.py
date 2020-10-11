from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='dora_explorer',
    version='0.2.2',
    description='Python project to get insights and distances to explore the places of the Earth',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    packages=find_packages(exclude=("tests", 'images')),
    author='Mohammed Sameeruddin',
    author_email='msameeruddin1998@gmail.com',
    keywords=['Geo-Explorer', 'Python Explorer', 'Geo-Traveller', 'Python 3'],
    url='https://github.com/msameeruddin/dora_explorer',
)

install_requires = [
    'plotly', 
    'mpu', 
    'unidecode', 
    'geonamescache',
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)