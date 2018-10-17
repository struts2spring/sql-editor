import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    with open(os.path.join('src', '__init__.py')) as f:
        for line in f:
            if line.strip().startswith('__version__'):
                return eval(line.split('=')[-1])


setuptools.setup(
    name="sql_editor",
    version=get_version(),
    author="Vijay",
    author_email="certifyexam0@gmail.com",
    description="A graphic SQLite Editor in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['sqlite', 'gui', 'wxpython', 'sql'],
    url="https://github.com/struts2spring/sql-editor",
    packages=setuptools.find_packages(),
    install_requires=[
        'pypubsub==4.0.0',
        'six==1.11.0',
        'sqlalchemy==1.2.12',
        'wxpython==4.0.3',
        'sqlparse'
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'sql_editor = src.sql_editor:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    package_data={'src.images': ['*.png']},
    include_package_data=True
)
