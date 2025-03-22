from setuptools import setup, find_packages

setup(
    name="style-up",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "google-generativeai",
        "appwrite",
    ],
)