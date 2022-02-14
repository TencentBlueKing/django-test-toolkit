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
from django_test_toolkit.data_generation.faker_generator import DjangoModelFakerFactory
from settings import TEST_TOOLKIT_FAKER_CONFIG


class DynamicMockObject:
    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)


class MockValidator(DynamicMockObject):
    def __init__(self, code, limit_value, **kwargs):
        self.code = code
        self.limit_value = limit_value
        super().__init__(**kwargs)


class MockField(DynamicMockObject):
    pass


class MockModelDjangoFactory(DjangoModelFakerFactory):
    field_to_faker_config = TEST_TOOLKIT_FAKER_CONFIG
