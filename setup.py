from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="xmind2md",
    version="0.1",
    install_requires=requirements,
    entry_points=f"""
        [console_scripts]
        xmind2md=xmind2md.xmind2md:main
    """,
)
