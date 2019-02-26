import setuptools

pkg_name="codepod"

setuptools.setup(
    name=pkg_name,
    version="0.1.4",
    author="Jeremy Magland",
    author_email="jmagland@flatironinstitute.org",
    description="Open code workspaces in docker for editing via containerized vscode",
    url="https://github.com/magland/codepod",
    packages=setuptools.find_packages(),
    scripts=['bin/codepod'],
    package_data={},
    install_requires=[
        "pyyaml",
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)
