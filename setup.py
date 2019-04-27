try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open
import sys

setup(
    name="seo_go",
    version="1.0.0",
    description="Command-line tool that automatically fetches Stack Overflow results after compiler errors",
    url="https://github.com/CANYOUFINDIT/SEO",
    author="CANYOUFINDIT",
    author_email="2505888537@qq.com",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "Programming Language :: Python"
    ],
    include_package_data=True,
    packages=["seo"],
    entry_points={"console_scripts": ["seo = seo.seo:main"]},
    install_requires=["BeautifulSoup4", "requests", "npyscreen"],
    requires=["BeautifulSoup4", "requests", "npyscreen"],
    python_requires=">=2.7"
)