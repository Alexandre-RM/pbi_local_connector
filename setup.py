from setuptools import setup, find_packages

setup(
    name="pbi_local_connector",
    version="0.4",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description = "Provides utilities to read data from PowerBI dataset open locally",
    author="ARM",
    url="https://github.com/Alexandre-RM/pbi_local_connector",
    install_requires=["pandas", "pyadomd"]
)

#py setup.py sdist bdist_wheel
#twine upload --skip-existing dist/*

