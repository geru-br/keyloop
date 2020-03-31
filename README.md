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
### Create database permission to your system user
```
linux_user:~/keyloop$ sudo su postgresql
postgresql:~/keyloop$ psql

postgres=# create user "linux_user";
postgres=# alter user "linux_user" CREATEDB;
postgres=# \q

postgresql:~/keyloop$ exit
linux_user:~/keyloop$
```

### Create development and test DBs
```
linux_user:~/keyloop$ createdb keyloop.dev
linux_user:~/keyloop$ createdb keyloop.tests
```

### Initialize development
```
linux_user:~/keyloop$ initialize_keyloop_db development.ini
```

### Create migration
```
linux_user:~/keyloop$ alembic -c development.ini revision --autogenerate -m "<description>"
```

### Database upgrade to last version
```
linux_user:~/keyloop$ alembic -c development.ini upgrade head
```

### Database downgrade one version
###
```
linux_user:~/keyloop$ alembic -c development.ini downgrade -1
```
