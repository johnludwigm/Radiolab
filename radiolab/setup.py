
from setuptools import setup

setup(author="John Ludwig",
      author_email="johnludwigm@gmail.com",
      description="Download episodes of Radiolab as mp3 files to a specified directory.",
      keywords="radiolab podcast download episode Jad Abumrad Robert Krulwich WNYC",
      license="MIT",
      install_requires=[
        "bs4",
        "requests"
        ],
      name="radiolab",
      url="https://github.com/johnludwigm/Radiolab",
      packages=['radiolab'],
      version="0.1",
      zip_safe=False)
