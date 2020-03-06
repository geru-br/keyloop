master branch:

[![Build Status](https://api.travis-ci.org/debonzi/keyloop.svg?branch=master)](https://travis-ci.org/debonzi/keyloop)

development branch:

[![Build Status](https://api.travis-ci.org/debonzi/keyloop.svg?branch=development)](https://travis-ci.org/debonzi/keyloop)

last build

[![Build Status](https://api.travis-ci.org/debonzi/keyloop.svg)](https://travis-ci.org/debonzi/keyloop)

# Key Loop
## Development
 * Create a 3.7 python virtual env using you prefered tool and activate it

```
$ pip install -e .[dev]
$ pre-commit install
```

The code style is done by *black* and there is a pre-commit hook that runs it and will stop the commit in case changes are made by *black*. Black should be run before commit and the pre commit hook is there just to help you in case you forget it.
If that in mind, the workflow would be something like:

```
$ # Do your coding
$ black .
$ git diff # check your work
$ git add <files>
$ git commit
```


## Database

Keyloop is a library that does not _directly_ persist the data it uses,
and therefore, do not use any databases.
Library users are responsible to register data providers - callables implementing
the interfaces needed for the various functions - including endpoints
to work.

As not all of these interfaces need to be customized, an embedded extension
for KeyLoop is available at the /keyloop/ext/sqla subtree - those are models
using SQLAlchemy that can be extended and bound to a concrete database
by the user.

There is an example application at the /playground subtree that does exactly that.
TL;DR: in order to use keyloop without having to reimplement any models, schemas
or code that implement the needed interfaces, you should check and lift some code from the playground app
to implement the concrete SQLAlchemy-backed models in your own app.

### Create testing playground database

The above being said, for testing and "see it running" purposes, the playground app
is configured to create a minimal SQLITE database and pre-fill it
with needed objects.

```
linux_user:~/keyloop$ make playground-database
```
