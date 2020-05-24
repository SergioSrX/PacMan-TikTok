from setuptools import setup

setup(
    name='Pacman-TikTok',
    version='1.0',
    description='Crawling and analyzing data of users from TikTok platform',
    author='MIB team',
    packages=['Pacman-TikTok'],
    install_requires=['Naked', 'scrapy', 'pymongo', 'json', 'datetime', 'matplotlib', 'pandas']  # external packages as dependencies
)
