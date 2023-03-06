import setuptools

# Open the README.md file for long description.
with open('README.md', 'r', encoding='utf-8') as readme_file:
    longDescription = readme_file.read()

setuptools.setup(
    name="open_proxy",
    version="0.0.1",
    author="T.K.santhosh",
    author_email="python.santhosh.py@gmail.com",
    description="Get Free working proxies around the world.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/santhoshtk01/open-proxy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
