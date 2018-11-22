# !/bin/bash
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
export APP_NAME="$(basename $APP_HOME)"

. "${APP_HOME}/conf/default.conf"
. "${APP_HOME}/conf/env.conf"

# include log manipulation script start
. "${APP_HOME}"/libexec/log.sh
# include log manipulation script end


. "${APP_HOME}"/build_tool/build-utils.sh

LIB_PATH="${APP_HOME}"/lib

function usage()
{
    echo "[Installation]
    Usage: `basename $0` [OPTIONS] ENV (dev|ut|uat|prod)
     e.g. `basename $0` -p dev
    OPTIONS:
       -h|--help                             Show this message
       -b|--build                            Build project
       -c|--clean                            Clean last build result
       -r|--rebuild                          Rebuild Project
    "
}

args=`getopt -o hrbcd --long build,clean,rebuild,help \
     -n 'build.sh' -- "$@"`

if [ $? != 0 ] ; then
  echo "terminating..." >&2 ;
  exit 1 ;
fi
eval set -- "$args"


while true ; do
  case "$1" in
    -b|--build )
        BUILD_OPT="true" 
        shift
        ;;
    -c|--clean )
        CLEAN_OPT="true"
        shift
        ;;
    -r|--rebuild )
        BUILD_OPT="true" 
        CLEAN_OPT="true"
        shift
        ;;
    -h|--help )
        usage
        exit
        ;;
    --)
        shift ;
        break
        ;;
    *)
        echo "internal error!" ;
        exit 1
        ;;
  esac
done

for arg do
    ENV=$arg
done

# check for required args
if [[ -z ${ENV} ]] ; then
  echo "$(basename $0): missing ENV : ${ENV}"
  usage
  exit 1
fi


function clean_deps(){
    log_info "Start to Remove dependencies"
    clean_deps_func ${LIB_PATH}
}

function build_project()
{

    # check exists for ENV variable and config 
    if [[ -z ${ENV} ]] ; then
        echo "$(basename $0): missing ENV : ${ENV}"
        usage
        exit 1
    fi

    log_info "Start to build project"

    # TODO
    log_info "write ${ENV} to ENV arg in env.conf"

    build_py_project_func
}

function clean_project()
{
    
    log_info "Start to clean project"
    clean_project_func
}


# call function

if [[ -n $CLEAN_OPT ]]; then
    clean_project
fi

if [[ -n $BUILD_OPT ]]; then
    build_project
fi

