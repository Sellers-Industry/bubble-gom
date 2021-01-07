#
#   Copyright (C) 2021 Sellers Industry - All Rights Reserved
#   Unauthorized copying of this file, via any medium is strictly
#   prohibited. Proprietary and confidential.
#
#   author: Evan Sellers <sellersew@gmail.com>
#   date: Wed Jan 06 2021
#   file: setup.py
#   project: Bubble Gom (Go Manager)
#   purpose: Install Setup File
#
#


from setuptools import setup

setup(
    name="gom",
    version="0.0.1",
    packages=[ "gom" ],
    entry_points={
        "console_scripts": [
            "gom = gom.__main__:main"
        ]
    },
)