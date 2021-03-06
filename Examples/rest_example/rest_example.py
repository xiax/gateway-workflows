# Copyright 2017 BlueCat Networks (USA) Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# By: BlueCat Networks
# Date: 05-12-17
# Gateway Version: 17.10.1
# Description: Example Gateway workflows

from flask import request, g, jsonify

from bluecat import route, util
from main_app import app

# application config


#
# Example rest GET call
#
@route(app, '/rest_example/get_test')
@util.rest_workflow_permission_required('rest_example')
@util.rest_exception_catcher
def rest_get_test():
    # are we authenticated?
    # yes, build a simple JSON response
    res = {}
    res['username'] = g.user.get_username()
    configs = []
    for c in g.user.get_api().get_configurations():
        configs.append({'id': c.get_id(), 'name': c.get_name()})
    res['configs'] = configs
    return jsonify(res)


#
# Example rest PUT call
#
@route(app, '/rest_example/put_test')
@util.rest_workflow_permission_required('rest_example')
@util.rest_exception_catcher
def rest_put_test():
    return jsonify({'result': request.get_json()['foo'] + ' plus some extra'})
