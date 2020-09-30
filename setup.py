"""
       Copyright [2020] [Sinisa Seslak (seslaks@gmail.com)
    
       Licensed under the Apache License, Version 2.0 (the "License");
       you may not use this file except in compliance with the License.
       You may obtain a copy of the License at
    
       http://www.apache.org/licenses/LICENSE-2.0
    
       Unless required by applicable law or agreed to in writing, software
       distributed under the License is distributed on an "AS IS" BASIS,
       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
       See the License for the specific language governing permissions and
       limitations under the License.
"""

"""
       Setup file for CredPy package (https://github.com/seslak/CredPy)
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="credpy",
    version="0.9.1",
    author="Sinisa Seslak",
    author_email="seslaks@gmail.com",
    description="Credit risk library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    url="https://pypi.org/project/credpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
          'pandas',
          'scikit-learn'
      ],
    python_requires='>=3.6',
)