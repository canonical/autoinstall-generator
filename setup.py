import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="preseed_to_answers",
    version="0.0.1",
    author='Canonical Engineering',
    author_email='ubuntu-dev@lists.ubuntu.com',
    description="Conversion utility to create subiquity answers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbungert/preseed-to-answers",
    packages=setuptools.find_packages(),
    license="AGPLv3+",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8', # earlier versions not yet tested
)

