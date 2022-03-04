from distutils.core import setup

setup(

    # Application name:
    name="iamheadless_publisher_admin",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="Maris Erts",
    author_email="maris@plain.ie",

    # Packages
    packages=["iamheadless_publisher_admin"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="#",

    #
    # license="LICENSE.txt",
    description="#",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "Django==4.0.1",
        "djantic==0.4.1",
        "pydantic==1.9.0",
    ],

)
