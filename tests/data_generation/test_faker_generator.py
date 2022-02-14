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
import copy
from datetime import datetime
from unittest.mock import MagicMock

from django.test import TestCase

from django.db.models import fields

from data_generation.base import MockField, MockModelDjangoFactory, MockValidator
from django_test_app.models import TestFieldModel, TestFieldWithDefaultValueModel, TestFieldWithChoiceModel


class DjangoModelFakerFactoryTestCase(TestCase):
    def test__generate_model_field_data__no_constraints(self):
        generated_data = MockModelDjangoFactory._generate_model_field_data(model_class=TestFieldModel)
        self.assertIsInstance(generated_data, dict)
        self.assertTrue("test_field" in generated_data)
        self.assertIsInstance(generated_data["test_field"], int)

    def test__generate_model_field_data__default_value(self):
        generated_data = MockModelDjangoFactory._generate_model_field_data(model_class=TestFieldWithDefaultValueModel)
        self.assertIsInstance(generated_data, dict)
        self.assertTrue("test_field" in generated_data)
        self.assertEqual(generated_data["test_field"], -1)

    def test__generate_model_field_data__choices(self):
        generated_data = MockModelDjangoFactory._generate_model_field_data(model_class=TestFieldWithChoiceModel)
        self.assertIsInstance(generated_data, dict)
        self.assertTrue("test_field" in generated_data)
        self.assertIn(generated_data["test_field"], [choice[0] for choice in TestFieldWithChoiceModel.CHOICES])

    def test__generate_fake_data(self):
        test_fields = ["CharField", "TextField", "IntegerField", "DateTimeField"]
        generated_instance_types = [str, str, int, datetime]
        for test_field, generated_instance_type in zip(test_fields, generated_instance_types):
            field_faker_config = copy.deepcopy(MockModelDjangoFactory.field_to_faker_config["fields"][test_field])
            if "processing_func" in field_faker_config:
                field_faker_config.pop("processing_func")
            char_field = MockField(validators=[])
            faker_data, _, extra_kwargs = MockModelDjangoFactory._generate_fake_data(field_faker_config, char_field)
            self.assertIsInstance(faker_data, generated_instance_type)
            self.assertEqual(extra_kwargs, field_faker_config.get("extra_kwargs", {}))

    def test__check_and_retry_for_unique_field(self):
        GENERATED_VALUE = 5
        generate_func = MagicMock(return_value=GENERATED_VALUE)
        validators = [
            MockValidator(code="min_value", limit_value=5),
            MockValidator(code="max_value", limit_value=5),
        ]
        field = MockField(name="test_field", validators=validators, unique=True)
        tolerance_value = 10
        TestFieldModel(test_field=GENERATED_VALUE).save()
        retry_value = MockModelDjangoFactory._check_and_retry_for_unique_field(
            TestFieldModel, field, tolerance_value, GENERATED_VALUE, generate_func, func_kwargs={}
        )
        self.assertEqual(retry_value, GENERATED_VALUE)
        generate_func.assert_has_calls([{} for _ in range(tolerance_value)])

    def test__get_field_existing_values(self):
        TEST_FIELD_VALUES = [1, 2]
        for value in TEST_FIELD_VALUES:
            TestFieldModel(test_field=value).save()
        existing_values = MockModelDjangoFactory._get_field_existing_values(TestFieldModel, "test_field")
        self.assertEqual(list(existing_values), TEST_FIELD_VALUES)

    def test__generate_default_and_choices_value__not_match(self):
        field = MockField(default=fields.NOT_PROVIDED, choices=[])
        value, generated = MockModelDjangoFactory._generate_default_and_choices_value(field)
        self.assertEqual(value, None)
        self.assertEqual(generated, False)

    def test__generate_default_and_choices_value__with_default(self):
        field = MockField(default=5, choices=[])
        value, generated = MockModelDjangoFactory._generate_default_and_choices_value(field)
        self.assertEqual(value, 5)
        self.assertEqual(generated, True)

    def test__generate_default_and_choices_value__with_choice(self):
        CHOICES = ["a", "b", "c"]
        field = MockField(default=fields.NOT_PROVIDED, choices=CHOICES)
        value, generated = MockModelDjangoFactory._generate_default_and_choices_value(field)
        self.assertTrue(value in CHOICES)
        self.assertEqual(generated, True)
