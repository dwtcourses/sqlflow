# Copyright 2020 The SQLFlow Authors. All rights reserved.
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
"""This module saves or loads the SQLFlow model.
"""
import os
from enum import Enum

# TODO(yancey1989): move diag to the upper directory.
from runtime.tensorflow.diag import SQLFlowDiagnostic


class EstimatorType(Enum):
    """The enum type for various SQLFlow estimator.
    """
    TENSORFLOW = 1
    XGBOOST = 2


class Model:
    """Model module represents a SQLFlow trained model, which includes
    three parts:
    1. the estimator type indicates which SQLFlow estimator comes from.
    2. the model meta indicates the meta data of training .e.g attributions,
    feature column types.
    3. the model data indicated the trained model, which generated by the AI
    engine, .e.g TensorFlow, XGBoost.

    Usage:

        meta = runtime.collect_model_metadata(train_params={...},
                                              model_params={...})
        m = runtime.model.Model(ModelType.XGBOOST, meta)
        m.save(uri="sqlfs://mydatabase/mytable")

    """
    def __init__(self, typ, meta):
        """
        Args:

        typ: EstimatorType
            the enum value of EstimatorType.

        meta: JSON
            the training meta with JSON format.
        """
        self._typ = typ
        self._cwd = os.getcwd()
        self._meta = meta

    def save(self, uri, datasource=None):
        """ save this model object.
        Args:

        uri: string
            the URI represents where to save the model, the format
            is like <driver>://<path>. This save API supports
            "sqlfs" and "file" driver.

        datasource: string
            the connection datasource DSN is required if saving with sqlfs.
        """
        driver, path = parseURI(uri)
        if driver == "file":
            # TODO(yancey1989): save model with local file system.
            raise NotImplementedError
        elif driver == "sqlfs":
            # TODO(yancey1989): save model with SQL file system.
            raise NotImplementedError
        else:
            raise SQLFlowDiagnostic("unsupported driven to save model: %s" %
                                    driver)


def parseURI(uri):
    """Parse the model URI into two parts: driver and path.
    """
    array = uri.split("://")
    if len(array) != 2:
        raise SQLFlowDiagnostic("invalid model saving URI: {0},\
            which should be <driver>://<path>".format(uri))
    return array[0], array[1]


def load(uri, datasource=None):
    # TODO(yancey1989): load model object from model storage with uri.
    raise NotImplementedError