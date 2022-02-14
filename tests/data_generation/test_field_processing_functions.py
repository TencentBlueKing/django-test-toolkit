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
from django.test import TestCase

from django_test_toolkit.data_generation.constants import (
    PROCESSING_CHAR_FIELD_DEFAULT_MIN_LENGTH,
    PROCESSING_CHAR_FIELD_DEFAULT_MAX_LENGTH,
)
from django_test_toolkit.data_generation.field_processing_functions import (
    text_provider_char_field_processing,
    random_int_provider_integer_field_processing,
)
from tests.data_generation.base import MockValidator, MockField


class FieldProcessingTestCase(TestCase):
    def test_text_provider_char_field_processing__default(self):
        TEST_TIMES = 100
        MIN_LENGTH, MAX_LENGTH = (
            PROCESSING_CHAR_FIELD_DEFAULT_MIN_LENGTH,
            PROCESSING_CHAR_FIELD_DEFAULT_MAX_LENGTH,
        )
        field = MockField(validators=[])
        for _ in range(TEST_TIMES):
            result = text_provider_char_field_processing(field)
            self.assertTrue(MIN_LENGTH <= result["max_nb_chars"] <= MAX_LENGTH)

    def test_text_provider_char_field_processing__appointed(self):
        MIN_LENGTH = 2
        MAX_LENGTH = 5
        TEST_TIMES = 100
        validators = [
            MockValidator(code="min_length", limit_value=MIN_LENGTH),
            MockValidator(code="max_length", limit_value=MAX_LENGTH),
        ]
        field = MockField(validators=validators)
        for _ in range(TEST_TIMES):
            result = text_provider_char_field_processing(field)
            self.assertTrue(MIN_LENGTH <= result["max_nb_chars"] <= MAX_LENGTH)

    def test_random_int_provider_integer_field_processing__default(self):
        field = MockField(validators=[])
        result = random_int_provider_integer_field_processing(field)
        self.assertEqual(result, {})

    def test_random_int_provider_integer_field_processing__appointed(self):
        MIN_VALUE = 1
        MAX_VALUE = 10
        validators = [
            MockValidator(code="min_value", limit_value=MIN_VALUE),
            MockValidator(code="max_value", limit_value=MAX_VALUE),
        ]
        field = MockField(validators=validators)
        result = random_int_provider_integer_field_processing(field)
        self.assertEqual(result, {"min": MIN_VALUE, "max": MAX_VALUE})
