# -*- coding:utf-8 -*-
"""
自定义日志对象。
# author: Trico
# date: 2019.7.13
"""

import os
import logging.config
from logging import Logger


class LLog(Logger):
    # 自定义日志。

    def __init__(self, logger_name, log_path=None, only_console=False, logger_level="INFO"):
        """
        自定义日志。
        :param logger_name: 日志名称。
        :param log_path: 日志路径。
        :param only_console: 是否只输出至控制台。
        :param logger_level: 日志级别。
        """

        super(LLog, self).__init__(logger_name)

        # 日志对象名。
        if not logger_name or not isinstance(logger_name, str):
            raise ValueError("The 'logger_name' is not a type of str or empty.".format(logger_name))
        self._logger_name = logger_name

        # 是否只输出至屏幕。
        if only_console is True:
            self._only_console = True
        else:
            self._only_console = False

        # 日志存放路径。
        self._log_path = None
        if self._only_console is False:
            if log_path and isinstance(log_path, str):
                self._log_path = log_path
                if os.path.exists(log_path) and not os.path.isdir(log_path):
                    raise ValueError("{} is not a directory.".format(self._log_path))
                else:
                    self._log_path = os.path.join(self._log_path, logger_name)
                    os.makedirs(self._log_path, mode=0o755, exist_ok=True)

        # 日志级别。
        if self._check_level(logger_level):
            self._logger_level = logger_level
        else:
            raise ValueError("Unknown level: {}.".format(logger_level))

    @property
    def logger(self):
        """
        日志对象。
        :return:
        """

        if self._only_console:
            # 输出控制台。
            conf = self._console_conf()
            logging.config.dictConfig(conf)
        else:
            if self._log_path:
                # 输出日志文件和控制台。
                conf = self._default_conf()
                logging.config.dictConfig(conf)
            else:
                # 输出控制台。
                conf = self._console_conf()
                logging.config.dictConfig(conf)

        return logging.getLogger(self._logger_name)

    @staticmethod
    def _check_level(level):
        """
        检查日志等级。
        :param level:
        :return:
        """

        # 日志等级。
        levels = {
            'CRITICAL', 'FATAL', 'ERROR',
            'WARN', 'WARNING', 'INFO',
            'DEBUG', 'NOTSET',
        }
        if level and isinstance(level, str) and level in levels:
            return True
        else:
            raise ValueError("Unknown level: {}.".format(level))

    def _default_conf(self):
        """
        默认日志配置项。
        :return:
        """

        # normal_format = '%(asctime)s - %(process)d/%(thread)d [%(module)s:%(lineno)d] %(levelname)s: %(message)s'
        normal_format = '%(asctime)s - %(process)d [%(module)s:%(lineno)d] %(levelname)s: %(message)s'
        return {'version': 1,
                'disable_existing_loggers': True,
                'incremental': False,
                'formatters': {
                    'style': {'class': 'logging.Formatter',
                              'format': normal_format,
                              'datefmt': '%Y-%m-%d %H:%M:%S'}
                },
                'handlers': {
                    'console': {
                        'class': 'logging.StreamHandler',
                        'level': self._logger_level,
                        'formatter': 'style'},

                    'file': {
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'level': self._logger_level,
                        'formatter': 'style',
                        'filename': os.path.join(self._log_path, '{}.log'.format(self._logger_name)),
                        'encoding': 'utf-8',
                        'when': 'MIDNIGHT'
                    },
                },
                'loggers': {self._logger_name: {'handlers': ['console', 'file', ],
                                                'level': self._logger_level,
                                                'propagate': False}
                            },
                'root': {
                    'handlers': [],
                    'level': self._logger_level, }
                }

    def _console_conf(self):
        """
        默认日志配置项。
        :return:
        """

        # normal_format = '%(asctime)s - %(process)d/%(thread)d [%(module)s:%(lineno)d] %(levelname)s: %(message)s'
        normal_format = '%(asctime)s - %(process)d [%(module)s:%(lineno)d] %(levelname)s: %(message)s'
        return {'version': 1,
                'disable_existing_loggers': True,
                'incremental': False,
                'formatters': {
                    'style': {'class': 'logging.Formatter',
                              'format': normal_format,
                              'datefmt': '%Y-%m-%d %H:%M:%S'}
                },
                'handlers': {
                    'console': {
                        'class': 'logging.StreamHandler',
                        'level': self._logger_level,
                        'formatter': 'style'},
                },
                'loggers': {self._logger_name: {'handlers': ['console'],
                                                'level': self._logger_level,
                                                'propagate': False}
                            },
                'root': {
                    'handlers': [],
                    'level': self._logger_level, }
                }
