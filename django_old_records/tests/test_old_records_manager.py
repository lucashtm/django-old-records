from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from unittest.mock import Mock
from django.contrib.contenttypes.models import ContentType
from django_old_records.models import ModelConfig, FieldConfig
from django_old_records.tests.models import HardCodedModel, ModelWithConfig, ModelWithNoCreatedAt, ModelWithNoMaxAge, \
    ModelWithIntegerMaxAge
from random import randint

class OldRecordsManagerTest(TestCase):

    def setUp(self):
        self._timezone_now = timezone.now

    def test_model_with_no_max_age_never_returns_old_records(self):
        ModelWithNoMaxAge.objects.create()
        content_type = ContentType.objects.get_for_model(ModelWithNoMaxAge)
        self.assertEqual(ModelConfig.objects.filter(content_type=content_type).count(), 0)
        self.assertRaises(AttributeError, lambda: ModelWithNoMaxAge.max_age)
        self.assertEqual(ModelWithNoMaxAge.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + timedelta(days=365*10))
        self.assertEqual(ModelWithNoMaxAge.old_records.count(), 0)

    def test_model_with_no_created_at_field_does_not_return_old_records(self):
        ModelWithNoCreatedAt.objects.create()
        self.assertEqual(ModelWithNoCreatedAt.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + ModelWithNoCreatedAt.max_age)
        self.assertEqual(ModelWithNoCreatedAt.old_records.count(), 0)

    def test_hard_coded_max_age(self):
        HardCodedModel.objects.create()
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + HardCodedModel.max_age)
        HardCodedModel.objects.create()
        self.assertEqual(HardCodedModel.objects.count(), 2)
        self.assertEqual(HardCodedModel.old_records.count(), 1)

    def test_hard_coded_max_age_as_integer_translates_to_days(self):
        ModelWithIntegerMaxAge.objects.create()
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + timedelta(days=ModelWithIntegerMaxAge.max_age-1))
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=self._timezone_now() + timedelta(days=ModelWithIntegerMaxAge.max_age))
        ModelWithIntegerMaxAge.objects.create()
        self.assertEqual(ModelWithIntegerMaxAge.objects.count(), 2)
        self.assertEqual(ModelWithIntegerMaxAge.old_records.count(), 1)

    def test_model_config(self):
        content_type = ContentType.objects.get_for_model(ModelWithConfig)
        model_config = ModelConfig(content_type=content_type, max_age=timedelta(seconds=randint(10, 100)))
        model_config.save()
        ModelWithConfig.objects.create()
        self.assertEqual(ModelWithConfig.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + model_config.max_age)
        ModelWithConfig.objects.create()
        self.assertEqual(ModelWithConfig.objects.count(), 2)
        self.assertEqual(ModelWithConfig.old_records.count(), 1)

    def test_field_configs(self):
        content_type = ContentType.objects.get_for_model(ModelWithConfig)
        model_config = ModelConfig.objects.create(content_type=content_type)
        boolean_max_age = timedelta(seconds=randint(10, 100))
        field_config = FieldConfig.objects.create(
            model_config=model_config,
            field_name='boolean_field',
            value='False',
            max_age=boolean_max_age
        )
        ModelWithConfig.objects.create(boolean_field=False)
        ModelWithConfig.objects.create()
        self.assertEqual(ModelWithConfig.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + field_config.max_age)
        ModelWithConfig.objects.create(boolean_field=False)
        self.assertEqual(ModelWithConfig.objects.count(), 3)
        self.assertEqual(ModelWithConfig.old_records.count(), 1)

    def test_multiple_field_configs(self):
        content_type = ContentType.objects.get_for_model(ModelWithConfig)
        model_config = ModelConfig.objects.create(content_type=content_type)
        boolean_max_age = timedelta(seconds=randint(10, 100))
        integer_max_age = boolean_max_age/2
        boolean_field_config = FieldConfig.objects.create(
            model_config=model_config,
            field_name='boolean_field',
            value='False',
            max_age=boolean_max_age
        )
        integer_field_config = FieldConfig.objects.create(
            model_config=model_config,
            field_name='integer_field',
            value='1',
            max_age=integer_max_age
        )
        ModelWithConfig.objects.create(integer_field=1)
        ModelWithConfig.objects.create(boolean_field=False)
        self.assertEqual(ModelWithConfig.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + integer_field_config.max_age)
        ModelWithConfig.objects.create(integer_field=1)
        self.assertEqual(ModelWithConfig.objects.count(), 3)
        self.assertEqual(ModelWithConfig.old_records.count(), 1)
        timezone.now = Mock(return_value=self._timezone_now() + boolean_field_config.max_age)
        self.assertEqual(ModelWithConfig.objects.count(), 3)
        self.assertEqual(ModelWithConfig.old_records.count(), 3)

    def test_field_over_model_precedence(self):
        content_type = ContentType.objects.get_for_model(ModelWithConfig)
        model_config = ModelConfig.objects.create(content_type=content_type, max_age=timedelta(seconds=20))
        field_config = FieldConfig.objects.create(
            model_config=model_config,
            field_name='boolean_field',
            value='False',
            max_age=timedelta(seconds=10)
        )
        ModelWithConfig.objects.create(boolean_field=False)
        ModelWithConfig.objects.create()
        self.assertEqual(ModelWithConfig.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + field_config.max_age)
        self.assertEqual(ModelWithConfig.objects.count(), 2)
        self.assertEqual(ModelWithConfig.old_records.count(), 1)
        timezone.now = Mock(return_value=self._timezone_now() + model_config.max_age)
        self.assertEqual(ModelWithConfig.old_records.count(), 2)

    def test_hardcode_dismissed_when_model_config_exists(self):
        content_type = ContentType.objects.get_for_model(HardCodedModel)
        model_config = ModelConfig.objects.create(content_type=content_type, max_age=timedelta(seconds=30))
        self.assertGreater(model_config.max_age, HardCodedModel.max_age)
        HardCodedModel.objects.create()
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + HardCodedModel.max_age)
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=self._timezone_now() + model_config.max_age)
        self.assertEqual(HardCodedModel.old_records.count(), 1)

    def test_hardcode_dismissed_when_field_config_exists(self):
        content_type = ContentType.objects.get_for_model(HardCodedModel)
        model_config = ModelConfig.objects.create(content_type=content_type)
        field_config = FieldConfig.objects.create(
            model_config=model_config,
            field_name='boolean_field',
            value='False',
            max_age=timedelta(seconds=30)
        )
        self.assertGreater(field_config.max_age, HardCodedModel.max_age)
        HardCodedModel.objects.create(boolean_field=False)
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=timezone.now() + HardCodedModel.max_age)
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=self._timezone_now() + field_config.max_age)
        self.assertEqual(HardCodedModel.old_records.count(), 1)
