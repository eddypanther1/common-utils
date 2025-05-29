from setuptools import setup, find_packages

setup(
    name="common-utils",  # Package name (used in imports)
    version="0.1.0",      # Version number
    packages=find_packages(),  # Automatically include common_utils/ and its contents
    install_requires=["requests"],  # List dependencies if any (e.g., ["requests"])
    author="Eddy Panther",
    description="A collection of AI helper functions and utilities",
)