from setuptools import setup, find_packages

setup(
    name="pyreto",
    version="0.1.0",
    packages=find_packages(),
    py_modules=['main', 'color_store', 'color_utils'],
    install_requires=[
        "textual>=0.40.0",
        "pyperclip>=1.8.2",
    ],
    author="RDJeffery",
    author_email="your.email@example.com",
    description="A color palette management tool for Linux",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RDJeffery/pyreto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'pyreto=main:main',
        ],
    },
) 