from setuptools import setup
from setuptools import find_packages

setup(name="kerasvis",
    version="0.3.2",
    description="Visualize Keras optimizations live in your browser",
    author="Emmanuel Klinger",
    url="http://github.com/neuralyzer/kerasvis",
    author_email="emmanuel.klinger@gmail.com",
    license="GPL",
    classifier=['Programming Language :: Python :: 3'],
    keywords="keras optimization visualization",
    install_requires=["flask", "bokeh", "pandas", "SQLAlchemy"],
    packages=find_packages(),
    include_package_data = True)
