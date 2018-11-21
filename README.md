# pyspark project template

- create venv

```
virtualenv venv
```

- enter into virtual env

```
source venv/bin/activate
```

- install all libs in py_pkg in virtual env

```
python setup.py lib -p py_pkg
```

- install pkg in your module

```
python setup.py install
```

- leave venv and execute

```
deactivate
bin/start-job.sh
```

---

- test your project

```
# pytest
python setup.py test

# pytest with arguments
python setup.py test -a -vvv
```

- clean build files

```
# clean without .egg folder
python setup.py clean

# clean with .egg folder
python setup.py clean -e
```
