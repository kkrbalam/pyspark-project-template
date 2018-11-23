# pyspark project template

## 前置作業

若為 MacOS 需安裝與 linux 一致的 getopt

```bash
brew install gnu-getopt
echo 'export PATH="/usr/local/opt/gnu-getopt/bin:$PATH"' >> ~/.bash_profile
```

## 一鍵安裝

```sh
$ ./build_tool/build.sh -h
[Installation]
    Usage: build.sh [OPTIONS] ENV (dev|ut|uat|prod)
     e.g. build.sh -b dev
    OPTIONS:
       -h|--help                             Show this message
       -b|--build                            Build project
       -c|--clean                            Clean last build result
       -r|--rebuild                          Rebuild Project
```

- 執行 build

```
bin/build.sh -b dev
```

## 手動安裝

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

- leave venv

```
deactivate
```

## 啟動主程式

- execute

```
bin/start-job.sh
```

## 設定檔

### 確認各環境的設定檔 conf/\*.conf

- conf/env.conf

設定 `bin/start-job.sh` 執行時所需參數，e.g. `spark` 相關的資源參數

- runtime-env-info.sh

設定環境路徑

- job.conf

程式執行時的參數設定檔，可自行擴充，檔案  格式為 [hoconf](https://github.com/chimpler/pyhocon)

e.g.

```json
job.name=project-template
databases.active = true
databases.enable_logging = false
databases.home_dir = /Users/darthbear
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
