#!/usr/bin/env bash

# 引入环境变量。
export PY_PROJECT_HOME=/home/debugger/test_env/big_data/big_data_platform
#export PY_PROJECT_HOME=/home/quxing/product_env/big_data/big_data_platform
export LD_LIBRARY_PATH=/usr/local/python3.6/lib:${LD_LIBRARY_PATH}
#export PYTHONPATH=${PY_PROJECT_HOME}/apis/api_data_center/:${PYTHONPATH}
export PYTHONPATH=${PY_PROJECT_HOME}/apis/api_data_center/:${PYTHONPATH}

# 执行脚本。
/usr/bin/env python3 run_python_scripts.py $@
