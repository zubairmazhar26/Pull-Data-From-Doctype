from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in exchangedata/__init__.py
from exchangedata import __version__ as version

setup(
	name="exchangedata",
	version=version,
	description="Pull data of purchase invoice in new doctype",
	author="Muhammad Zubair",
	author_email="zubairmazhar23@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
