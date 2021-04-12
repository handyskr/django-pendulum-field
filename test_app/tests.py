import uuid

import pendulum
from django.core import serializers
from django.test import TestCase

from django_pendulum_field.form import PendulumField as PendulumFormField
from .forms import *
from .models import *


class ModelFieldTests(TestCase):
    def test_model_create_and_return(self):
        test_pk = str(uuid.uuid4())
        test_dt = pendulum.datetime(2021, 4, 13, 12, 24, 0, tz="UTC")
        Something.objects.create(id=test_pk, some_dt=test_dt)
        created_something = Something.objects.get(pk=test_pk)
        self.assertIsInstance(created_something.some_dt, pendulum.DateTime)
        self.assertEqual(created_something.some_dt, test_dt)

    def test_model_auto_now_add(self):
        now = pendulum.now()
        allowed_diff_minutes = 3
        test_pk = str(uuid.uuid4())
        created_something = SomethingWithAutoNowAdd.objects.create(id=test_pk)
        self.assertLessEqual((created_something.some_dt - now).in_minutes(), allowed_diff_minutes)
        created_something = SomethingWithAutoNowAdd.objects.get(pk=test_pk)
        self.assertLessEqual((created_something.some_dt - now).in_minutes(), allowed_diff_minutes)

    def test_model_auto_now(self):
        allowed_diff_minutes = 3
        test_pk = str(uuid.uuid4())
        SomethingWithAutoNow.objects.create(id=test_pk, some_dt=pendulum.datetime(2001, 1, 1))
        something = SomethingWithAutoNow.objects.get(pk=test_pk)
        something.dummy_field = "bye"
        something.save()
        now = pendulum.now()
        self.assertLessEqual((something.some_dt - now).in_minutes(), allowed_diff_minutes)
        something = SomethingWithAutoNow.objects.get(pk=test_pk)
        self.assertLessEqual((something.some_dt - now).in_minutes(), allowed_diff_minutes)

    def test_field_lookups(self):
        Something.objects.bulk_create(
            [
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1995, 1, 1, 1, 1, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1995, 1, 2, 1, 1, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1995, 1, 3, 1, 10, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1996, 1, 4, 2, 10, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1997, 1, 5, 2, 20, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1995, 3, 1, 1, 10, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1995, 3, 2, 1, 20, 1, tz="UTC")),
                Something(id=str(uuid.uuid4()), some_dt=pendulum.datetime(1995, 3, 3, 2, 1, 1, tz="UTC")),
            ]
        )

        self.assertEqual(
            Something.objects.filter(
                some_dt__gte=pendulum.datetime(1995, 1, 2, tz="UTC"),
                some_dt__lt=pendulum.datetime(1995, 3, 2, 1, 30, tz="Asia/Seoul"),
            ).count(),
            3,
        )
        self.assertEqual(
            Something.objects.filter(
                some_dt__year=1995,
            ).count(),
            6,
        )
        self.assertEqual(
            Something.objects.filter(
                some_dt__year__gte=1996,
                some_dt__year__lt=1997,
            ).count(),
            1,
        )

    def test_field_serialize(self):
        test_pk = str(uuid.uuid4())
        test_dt = pendulum.datetime(1998, 4, 12, 13, 42, 0, tz="UTC")
        test_pk2 = str(uuid.uuid4())
        test_dt2 = pendulum.datetime(1998, 4, 13, tz="UTC")
        Something.objects.create(id=test_pk, some_dt=test_dt)
        Something.objects.create(id=test_pk2, some_dt=test_dt2)
        data = serializers.serialize("json", Something.objects.filter(some_dt__year=1998).order_by("some_dt").all())
        result = list(serializers.deserialize("json", data))
        self.assertEqual(result[0].object.some_dt, test_dt)


class FormFieldTests(TestCase):
    def setUp(self):
        self.test_dt = pendulum.datetime(2021, 4, 11, 14, 18, tz="UTC")
        self.something = Something.objects.create(
            id=str(uuid.uuid4()),
            some_dt=self.test_dt,
        )
        self.something_form = SomethingForm(instance=self.something)

    def test_form_field_auto_use(self):
        self.assertEqual(self.something_form.fields["some_dt"].__class__, PendulumFormField)

    def test_form_render(self):
        self.something_form.as_p()

    def test_form_strptime(self):
        new_form = SomethingForm(
            {
                "id": str(uuid.uuid4()),
                "some_dt": self.test_dt.to_iso8601_string(),
            }
        )
        self.assertTrue(new_form.is_valid())
        self.assertEqual(new_form.cleaned_data["some_dt"], self.test_dt)
