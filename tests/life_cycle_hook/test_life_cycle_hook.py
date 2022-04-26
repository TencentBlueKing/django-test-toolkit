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
from django_test_toolkit.mixins.base import LifeCycleHooksMixin
from django_test_toolkit.testcases import ToolkitTestCase


class LifeCycleTestMixin(LifeCycleHooksMixin):
    @classmethod
    def set_up_test_data(cls):
        cls.set_up_test_data_value = "set_up_test_data_value"

    @classmethod
    def set_up_class(cls):
        cls.set_up_class_value = "set_up_class_value"

    def set_up(self):
        self.set_up_value = "set_up_value"


class LifeCycleHookTestCase(ToolkitTestCase, LifeCycleTestMixin):
    def test_life_cycle_hook(self):
        self.assertEqual(self.set_up_test_data_value, "set_up_test_data_value")
        self.assertEqual(self.set_up_class_value, "set_up_class_value")
        self.assertEqual(self.set_up_value, "set_up_value")


class ChildLifeCycleHookTestCase(LifeCycleHookTestCase):
    def setUp(self):
        super().setUp()
        self.child_set_up_value = "child_set_up_value"

    def test_parent_life_cycle_hook(self):
        self.test_life_cycle_hook()
        self.assertEqual(self.child_set_up_value, "child_set_up_value")
