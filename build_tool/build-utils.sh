# !/bin/bash

function build_basic_project_func()
{
    cd "${APP_HOME}"
    log_info "[BUILD] mkdir $APP_HOME/var"
    mkdir -p $APP_HOME/var

    log_info "[BUILD] mkdir $APP_HOME/var/logs"
    mkdir -p $APP_HOME/var/logs
}

function build_py_project_func()
{
    log_info "[BUILD] Start to build $APP_NAME "

    build_basic_project_func

    cd "${APP_HOME}"

    install_virtualenv

    install_py_common_pkg

    install_py_project

}

function install_virtualenv()
{

    log_info "create python2.7 venv : $PY_VENV"
    virtualenv -p python2.7 --no-setuptools --no-wheel --never-download $PY_VENV

    # enter virtualenv
    source ${PY_VENV}/bin/activate

    log_info "upgrade pip in venv"
    log_info "${BUILD_PY_PROXY} : ${BUILD_PY_PROXY}"
    ${PY_VENV}/bin/pip install --upgrade pip --disable-pip-version-check --no-cache-dir ${BUILD_PY_PROXY}

    log_info "install setuptools wheel in venv"
    ${PY_VENV}/bin/pip install setuptools wheel --disable-pip-version-check --no-cache-dir ${BUILD_PY_PROXY}

    # exit virtualenv
    deactivate

}

function install_py_setuptool()
{
    pkg_name=$1
    pkg_path=$2
    # enter virtualenv
    source ${PY_VENV}/bin/activate

    # install py_pkg by setup.py
    log_info "install $pkg_name by setup.py"
    cd $pkg_path
    python setup.py install

    # clean .egg folder or file
    log_info "run setup.py clean -e"
    cd $pkg_path
    python setup.py clean -e
    # exit virtualenv
    deactivate
}

function install_py_common_pkg()
{
    # install py_pkg
    for pkg in ${APP_HOME}/py_pkg/*
    do
        pkg_name="$(basename $pkg)"

        install_py_setuptool $pkg_name $pkg
    done

}

function install_py_project()
{
    install_py_setuptool $APP_NAME $APP_HOME
}


function clean_project_func()
{

    if [ -d "$PY_VENV" ]; then
        log_info "[CLEAN] clean root project $APP_NAME, delete dir $PY_VENV"
        rm -rf "$PY_VENV"
    fi
}

