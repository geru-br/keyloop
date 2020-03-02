from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

requires = [
    "arrow==0.15.5",
    "pyramid==1.10.4",
    "pyramid-tm==2.4",
    "gunicorn==20.0.4",
    "marshmallow==2.19.5",
    "marshmallow-enum==1.5.1",
    "cornice==4.0.1",
    "SQLAlchemy[postgresql_psycopg2binary]==1.3.13",
    "zope.sqlalchemy==1.2",
    "SQLAlchemy-Utils==0.36.1",
    "pyramid-ipython==0.2",
    "alembic==1.3.3",
    "marshmallow-jsonapi==0.23.0",
    "cornice-apispec==0.9.3",
    "click",
]

test_requires = [
    "pytest",
    "pytest-cov",
    "WebTest==2.0.33",
    "freezegun==0.3.13",
    "factory-boy==2.12.0",
    "pyresttest==1.7.1",
    "locust==0.0.0",
    "locustio==0.14.4",
]

ci_requires = [
    "python-coveralls",
]

dev_requires = [
    "black",
    "pre-commit",
    "pylint",
]

sqla = ["sqlalchemy"]


extras_require = {
    "sqla": sqla,
    "test": sqla + test_requires,
    "dev": sqla + test_requires + dev_requires,
    "ci": sqla + test_requires + ci_requires,
}

setup(
    name="keyloop",
    version="0.0.1",
    description="Key Loop - Authorization Server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Debonzi",
    author_email="debonzi@gmail.com",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requires,
    extras_require=extras_require,
    url="https://github.com/debonzi/keyloop",
    packages=["keyloop", ],
    entry_points={
        "paste.app_factory": ["main = keyloop:main", ],
        "console_scripts": [
            "kloop = keyloop.command.main:main",
            "initialize_keyloop_db = keyloop.models.initialize_db:main",
        ],
    },
)
