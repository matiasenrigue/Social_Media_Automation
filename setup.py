from setuptools import setup, find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name = "SocialMedia",
      description="Package to automate Social Media",
      packages=find_packages(),
      install_requires = requirements)
