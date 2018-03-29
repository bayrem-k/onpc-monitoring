#!/usr/bin/python
# Copyright 2015 Mirantis, Inc.
# Copyright 2018, OpenNext SAS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple
import logging
import os


log_level = logging.INFO
if os.getenv('COLLECTD_DEBUG', '') == 'True':
    log_level = logging.DEBUG
logging.basicConfig(
    level=log_level,
    format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s'
)

class Values(object):

    def __init__(self, values=None, plugin_instance=None, type_instance=None,
                 type=None, plugin=None, host=None, time=None,
                 meta=None, interval=None):
        self._values = values
        self._plugin_instance = plugin_instance
        self._type = type,
        self._type_instance = type_instance,
        self._plugin = plugin
        self._host = host
        self._time = time
        self._meta = meta
        self._interval = interval

    def dispatch(self, type=None, values=None, plugin_instance=None,
                 type_instance=None, plugin=None, host=None, time=None,
                 meta=None, interval=None):
        info("dispatch: plugin={plugin} plugin_instance={plugin_instance} "
             "type_instance={type_instance} "
             "host={host} interval={interval} "
             "values={values} meta={meta}".format(
                 plugin=plugin or self._plugin,
                 plugin_instance=plugin_instance or self._plugin_instance,
                 type_instance=type_instance or self._type_instance,
                 host=host or self._host,
                 interval=interval or self._interval,
                 values=values or self._values,
                 meta=meta or self._meta,
             ))


def load_configuration(plugin):
    collectd_vars = {
        e: os.environ[e]
        for e in os.environ.keys() if e.startswith('COLLECTD_')}
    for varname, value in collectd_vars.iteritems():
        debug("configuration: {}={}".format(varname, value))
        setattr(plugin, varname[9:].lower(), value)

    FakeConfig = namedtuple('FakeConfig', ['children'])
    plugin.config_callback(FakeConfig(children=[]))


def error(msg):
    logging.error(msg)

def warning(msg):
    logging.warning(msg)

def notice(msg):
    logging.info(msg)

def info(msg):
    logging.info(msg)

def debug(msg):
    logging.debug(msg)