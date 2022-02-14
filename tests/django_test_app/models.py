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

from django.db import models


class TestFieldModel(models.Model):
    test_field = models.IntegerField()


class TestFieldWithDefaultValueModel(models.Model):
    test_field = models.IntegerField(default=-1)


class TestFieldWithChoiceModel(models.Model):
    CHOICES = [(0, "value0"), (1, "value1")]
    test_field = models.IntegerField(choices=CHOICES)
