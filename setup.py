from setuptools import setup, find_packages

setup(
    name="GFMDiagrams",
    version="0.2.0",
    url="https://github.com/cookpad/gfm-diagram",
    author="Ben Howes",
    description="Mermaid in GitHub markdown",
    package_dir={"": "."},
    packages=["gfmd"],
    install_requires=["marko<2", "watchdog<2"],
    entry_points={"console_scripts": ["gfmd=gfmd:run"]},
)
