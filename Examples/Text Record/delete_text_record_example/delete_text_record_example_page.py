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

# Various Flask framework items.
import os
import sys

from flask import url_for, redirect, render_template, flash, g, request

from bluecat import route, util
import config.default_config as config
from main_app import app
from .delete_text_record_example_form import GenericFormTemplate


def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(unicode(__file__, encoding)))


# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/delete_text_record_example/delete_text_record_endpoint')
@util.workflow_permission_required('delete_text_record_example_page')
@util.exception_catcher
def delete_text_record_delete_text_record_page():
    form = GenericFormTemplate()
    # Remove this line if your workflow does not need to select a configuration
    form.configuration.choices = util.get_configurations(default_val=True)
    return render_template('delete_text_record_example_page.html',
                           form=form,
                           text=util.get_text(module_path(), config.language),
                           options=g.user.get_options())


@route(app, '/delete_text_record_example/form', methods=['POST'])
@util.workflow_permission_required('delete_text_record_example_page')
@util.exception_catcher
def delete_text_record_delete_text_record_page_form():
    form = GenericFormTemplate()
    # Remove this line if your workflow does not need to select a configuration
    form.configuration.choices = util.get_configurations(default_val=True)
    if form.validate_on_submit():
        try:
            # Retrieve form attributes
            text_record = g.user.get_api().get_entity_by_id(request.form['txt_list'])

            # Retrieve attributes for flash message
            text_record_name = text_record.get_property('absoluteName')
            text_record_id = util.safe_str(text_record.get_id())

            # Delete record
            text_record.delete()

            # Put form processing code here
            g.user.logger.info('Success-Text Record: ' + text_record_name + ' Deleted with Object ID: ' + text_record_id)
            flash('Success - Text Record: ' + text_record_name + ' Deleted with Object ID: ' + text_record_id, 'succeed')
            return redirect(url_for('delete_text_record_exampledelete_text_record_delete_text_record_page'))
        except Exception as e:
            flash(util.safe_str(e))
            # Log error and render workflow page
            g.user.logger.warning('%s' % util.safe_str(e), msg_type=g.user.logger.EXCEPTION)
            form.txt_filter.data = ''
            return render_template('delete_text_record_example_page.html',
                                   form=form,
                                   text=util.get_text(module_path(), config.language),
                                   options=g.user.get_options())
    else:
        g.user.logger.info('Form data was not valid.')
        form.txt_filter.data = ''
        return render_template('delete_text_record_example_page.html',
                               form=form,
                               text=util.get_text(module_path(), config.language),
                               options=g.user.get_options())
