from setuptools import setup, find_packages

setup(
    name="GFMDiagrams",
    version="0.1.0",
    url="https://github.com/cookpad/gfm-diagram",
    author="Ben Howes",
    description="Mermaid in GitHub markdown",
    package_dir={"": "."},
    packages=["gfmd"],
    install_requires=["marko<1.0", "watchdog"],
    entry_points={"console_scripts": ["gfmd=gfmd:run"]},
)
