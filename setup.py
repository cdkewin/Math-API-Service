from setuptools import setup, find_packages
#pip install -e


setup(
    name="math_api_service",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)