
from setuptools import setup, find_packages

with open( "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crypto-dice-game",
    version="1.0.0",
    author="Student Project",
    description="A cryptographically secure dice game with HMAC-SHA3 verification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[

        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "dice-game=main:main",
        ],
    },
)