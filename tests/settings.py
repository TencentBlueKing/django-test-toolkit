# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import os
import copy

from django_test_toolkit.data_generation.config import DEFAULT_FIELD_TO_FAKER_CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "django-test-toolkit"

INSTALLED_APPS = ["django_test_app"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "TEST": {"NAME": os.path.join("test_db.sqlite3")},
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEST_TOOLKIT_FAKER_CONFIG = copy.deepcopy(DEFAULT_FIELD_TO_FAKER_CONFIG)
TEST_TOOLKIT_FAKER_CONFIG["default_value_factor"] = 1
