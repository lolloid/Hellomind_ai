from unittest.mock import patch

from django.test import TestCase

from apps.ai_services.services import AIReplyResult
from apps.authentication.models import User
from apps.chat.models import Chat, Message
from apps.chat.services import build_messages, process_chat_message


class ChatGreetingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="greeting_user",
            email="greeting@example.com",
            password="testpass123",
        )

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_first_simple_greeting_goes_through_provider(self, mock_generate):
        mock_generate.return_value = AIReplyResult(reply="Hai juga, senang kamu mampir. Gimana harimu?", status="ok")

        result = process_chat_message(self.user, {"message": "hallo", "language": "id"})

        self.assertIn("Hai", result["reply"])
        self.assertNotIn("ceritain lagi", result["reply"].lower())
        self.assertEqual(result["response_source"], "groq")
        mock_generate.assert_called_once()
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 2)

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_greeting_after_emotional_context_can_use_ai_context(self, mock_generate):
        mock_generate.return_value = AIReplyResult(reply="Hai, aku masih di sini. Gimana rasanya sekarang?", status="ok")
        chat = Chat.objects.create(user=self.user, title="sedih")
        Message.objects.create(
            chat=chat,
            role=Message.ROLE_USER,
            text="aku sedih banget",
            text_emotion="sad",
            mood_score=-0.6,
        )

        result = process_chat_message(
            self.user,
            {"message": "hallo", "language": "id", "chat_id": chat.id},
        )

        self.assertEqual(result["reply"], "Hai, aku masih di sini. Gimana rasanya sekarang?")
        self.assertEqual(result["response_source"], "groq")
        mock_generate.assert_called_once()

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_off_topic_message_goes_through_provider_with_soft_context(self, mock_generate):
        mock_generate.return_value = AIReplyResult(
            reply="Bisa, tapi aku tetap paling cocok nemenin kamu ngobrol soal yang lagi kamu rasain.",
            status="ok",
        )

        result = process_chat_message(self.user, {"message": "bantu ngoding", "language": "id"})

        self.assertEqual(result["response_source"], "groq")
        mock_generate.assert_called_once()
        messages = mock_generate.call_args.args[0]
        self.assertTrue(any("di luar fokus utama" in message["content"] for message in messages))

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_provider_failure_uses_supportive_fallback(self, mock_generate):
        mock_generate.return_value = AIReplyResult(status="rate_limited", fallback_reason="rate_limited")

        result = process_chat_message(self.user, {"message": "aku takut gagal", "language": "id"})

        self.assertIn("takut gagal", result["reply"].lower())
        self.assertNotIn("ceritain lagi", result["reply"].lower())
        self.assertEqual(result["response_source"], "local_fallback")
        mock_generate.assert_called_once()

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_provider_failure_fallback_varies_by_user_message(self, mock_generate):
        mock_generate.return_value = AIReplyResult(status="rate_limited", fallback_reason="rate_limited")

        tired = process_chat_message(self.user, {"message": "aku capek", "language": "id"})
        anxious = process_chat_message(self.user, {"message": "aku overthinking terus", "language": "id"})

        self.assertNotEqual(tired["reply"], anxious["reply"])
        self.assertIn("capek", tired["reply"].lower())
        self.assertIn("overthinking", anxious["reply"].lower())
        self.assertEqual(tired["response_source"], "local_fallback")
        self.assertEqual(tired["fallback_reason"], "rate_limited")

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_casual_mishap_goes_through_provider(self, mock_generate):
        mock_generate.return_value = AIReplyResult(reply="WKWK aduh, jatuh depan orang tuh malu duluan ya.", status="ok")

        result = process_chat_message(self.user, {"message": "WKWK tadi aku jatuh", "language": "id"})

        self.assertIn("jatuh", result["reply"].lower())
        self.assertIn("WKWK", result["reply"])
        self.assertEqual(result["response_source"], "groq")
        mock_generate.assert_called_once()

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_quiet_user_fallback_is_not_pushy(self, mock_generate):
        mock_generate.return_value = AIReplyResult(status="rate_limited", fallback_reason="rate_limited")

        result = process_chat_message(self.user, {"message": "males cerita", "language": "id"})

        self.assertIn("nggak harus cerita sekarang", result["reply"].lower())
        self.assertNotIn("kenapa", result["reply"].lower())

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_provider_failure_keeps_persona_style(self, mock_generate):
        mock_generate.return_value = AIReplyResult(status="rate_limited", fallback_reason="rate_limited")
        self.user.ai_persona = "Chaos Friend, heboh, reactive, playful, exaggerated naturally"
        self.user.save(update_fields=["ai_persona"])

        result = process_chat_message(self.user, {"message": "aku dimarahin dosen", "language": "id"})

        self.assertIn("YAAMPUN", result["reply"])
        self.assertIn("dosen", result["reply"])

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_casual_embarrassment_goes_through_provider(self, mock_generate):
        mock_generate.return_value = AIReplyResult(
            reply="WKWK aduh salah masuk kelas tuh paniknya beda, pasti pengen langsung keluar pelan-pelan.",
            status="ok",
        )
        self.user.ai_persona = "Chill Bestie, santai, suka pakai WKWK, teman tongkrongan"
        self.user.save(update_fields=["ai_persona"])

        result = process_chat_message(self.user, {"message": "WKWK tadi aku salah masuk kelas", "language": "id"})

        self.assertIn("WKWK", result["reply"])
        self.assertIn("salah masuk kelas", result["reply"])
        self.assertEqual(result["response_source"], "groq")
        mock_generate.assert_called_once()

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_sleep_followup_goes_through_provider_with_history(self, mock_generate):
        mock_generate.return_value = AIReplyResult(
            reply="Lah pantes capeknya makin kerasa, tidur juga lagi nggak ngasih kamu pulih.",
            status="ok",
        )
        chat = Chat.objects.create(user=self.user, title="capek")
        Message.objects.create(
            chat=chat,
            role=Message.ROLE_USER,
            text="aku capek",
            text_emotion="sad",
            mood_score=-0.2,
        )
        self.user.ai_persona = "Chaos Friend, heboh, reactive, playful"
        self.user.save(update_fields=["ai_persona"])

        result = process_chat_message(
            self.user,
            {"message": "aku susah tidur juga", "language": "id", "chat_id": chat.id},
        )

        self.assertIn("pantes", result["reply"].lower())
        self.assertIn("tidur", result["reply"].lower())
        self.assertEqual(result["response_source"], "groq")
        mock_generate.assert_called_once()

    def test_build_messages_includes_latest_once_and_keeps_history_roles(self):
        chat = Chat.objects.create(user=self.user, title="history")
        Message.objects.create(chat=chat, role=Message.ROLE_USER, text="aku capek")
        Message.objects.create(chat=chat, role=Message.ROLE_BOT, text="pantes kamu lelah")
        Message.objects.create(chat=chat, role=Message.ROLE_USER, text="aku overthinking terus")

        messages = build_messages(chat, "SYSTEM", "aku overthinking terus")

        self.assertEqual(messages[0], {"role": "system", "content": "SYSTEM"})
        self.assertEqual(messages[1], {"role": "user", "content": "aku capek"})
        self.assertEqual(messages[2], {"role": "assistant", "content": "pantes kamu lelah"})
        self.assertEqual(messages[3]["role"], "system")
        self.assertIn("pesan terbaru", messages[3]["content"])
        self.assertEqual(messages[4], {"role": "user", "content": "aku overthinking terus"})
        self.assertEqual(
            sum(1 for message in messages if message["content"] == "aku overthinking terus"),
            1,
        )

    @patch("apps.chat.services.generate_chat_reply_result")
    def test_repetitive_provider_reply_is_replaced_by_contextual_fallback(self, mock_generate):
        repeated = "Aku di sini. Kita bisa ngobrol pelan-pelan, santai aja, tanpa harus langsung nemu jawaban."
        chat = Chat.objects.create(user=self.user, title="repeat")
        Message.objects.create(chat=chat, role=Message.ROLE_USER, text="aku sedih")
        Message.objects.create(chat=chat, role=Message.ROLE_BOT, text=repeated)
        mock_generate.return_value = AIReplyResult(reply=repeated, status="ok")

        result = process_chat_message(
            self.user,
            {"message": "aku overthinking terus", "language": "id", "chat_id": chat.id},
        )

        self.assertNotEqual(result["reply"], repeated)
        self.assertIn("overthinking", result["reply"].lower())
        self.assertEqual(result["response_source"], "local_fallback")
        self.assertEqual(result["fallback_reason"], "repetitive_provider_reply")
