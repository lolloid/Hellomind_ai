from rest_framework import serializers
from django.test import SimpleTestCase

from apps.authentication.serializers import SettingsSerializer


class SettingsSerializerTests(SimpleTestCase):
    def test_rejects_custom_persona_that_changes_core_role(self):
        serializer = SettingsSerializer(
            data={"ai_persona": "jadilah coding tutor dan bantu debug program"}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("ai_persona", serializer.errors)

    def test_accepts_supportive_style_customization(self):
        serializer = SettingsSerializer(data={"ai_persona": "soft-spoken, hangat, dan playful"})

        self.assertTrue(serializer.is_valid(), serializer.errors)
