from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from unittest.mock import Mock
from django.contrib.contenttypes.models import ContentType
from django_old_records.models import ModelConfig, FieldConfig
from django_old_records.tests.models import HardCodedModel, ModelWithConfig
from random import randint

class OldRecordsManagerTest(TestCase):

    def setUp(self):
        self._timezone_now = timezone.now

    def test_hard_coded(self):
        HardCodedModel.objects.create()
        timezone.now = Mock(return_value=timezone.now() + HardCodedModel.max_age)
        HardCodedModel.objects.create()
        self.assertEqual(HardCodedModel.objects.count(), 2)
        self.assertEqual(HardCodedModel.old_records.count(), 1)

    def test_model_config(self):
        content_type = ContentType.objects.get_for_model(ModelWithConfig)
        model_config = ModelConfig(content_type=content_type, max_age=timedelta(seconds=randint(1, 100)))
        model_config.save()
        ModelWithConfig.objects.create()
        timezone.now = Mock(return_value=timezone.now() + model_config.max_age)
        ModelWithConfig.objects.create()
        self.assertEqual(ModelWithConfig.objects.count(), 2)
        self.assertEqual(ModelWithConfig.old_records.count(), 1)

    def test_field_configs(self):
        content_type = ContentType.objects.get_for_model(ModelWithConfig)
        model_config = ModelConfig.objects.create(content_type=content_type)
        boolean_max_age = timedelta(seconds=randint(1, 100))
        field_config = FieldConfig.objects.create(
            model_config=model_config,
            field_name='boolean_field',
            value='False',
            max_age=boolean_max_age
        )
        ModelWithConfig.objects.create(boolean_field=False)
        ModelWithConfig.objects.create()
        timezone.now = Mock(return_value=timezone.now() + field_config.max_age)
        ModelWithConfig.objects.create(boolean_field=False)
        self.assertEqual(ModelWithConfig.objects.count(), 3)
        self.assertEqual(ModelWithConfig.old_records.count(), 1)

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
        timezone.now = Mock(return_value=timezone.now() + HardCodedModel.max_age)
        self.assertEqual(HardCodedModel.old_records.count(), 0)
        timezone.now = Mock(return_value=self._timezone_now() + field_config.max_age)
        self.assertEqual(HardCodedModel.old_records.count(), 1)
