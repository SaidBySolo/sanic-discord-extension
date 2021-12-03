import os

from setuptools import setup

import sanic_discord_extension

version = sanic_discord_extension.__version__

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

requirements = []
with open(f"{path}/requirements.txt", encoding="UTF8") as f:
    requirements = f.read().splitlines()

if not version:
    raise RuntimeError("version is not defined")

readme = ""
with open(f"{path}/README.md", encoding="UTF8") as f:
    readme = f.read()

setup(
    name="sanic_discord_extension",
    author="SaidBySolo",
    url="https://github.com/sanic_discord_extension/sanic_discord_extension",
    project_urls={
        "Source": "https://github.com/saidbysolo/sanic_discord_extension",
    },
    version=version,
    packages=["sanic_discord_extension", "sanic_discord_extension.discord", "sanic_discord_extension.discord.types"],
    license="MIT",
    description="sanic_discord_extension",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    package_data={"sanic_discord_extension": ["py.typed"], "sanic_discord_extension.discord": ["py.typed"], "sanic_discord_extension.discord.types": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)