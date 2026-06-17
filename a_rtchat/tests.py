from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ChatGroup, GroupMessage
from .rag import LocalRag, LocalRagError, RagAnswer


class ChatViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password",
        )
        self.client.force_login(self.user)

    def test_htmx_chat_submission_creates_user_and_bot_messages(self):
        rag = Mock()
        rag.answer.return_value = RagAnswer("Paris is the capital.", ("notes.md",))

        with patch("a_rtchat.views.LocalRag.from_settings", return_value=rag):
            response = self.client.post(
                reverse("home"),
                {"body": "What is the capital of France?"},
                HTTP_HX_REQUEST="true",
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ChatGroup.objects.filter(group_name="ai-chat").exists())
        self.assertTrue(User.objects.filter(username="botty").exists())
        self.assertEqual(GroupMessage.objects.count(), 2)
        self.assertTrue(GroupMessage.objects.filter(body__contains="Sources: notes.md").exists())

    def test_rag_failure_is_saved_as_friendly_bot_reply(self):
        rag = Mock()
        rag.answer.side_effect = LocalRagError("network down")

        with patch("a_rtchat.views.LocalRag.from_settings", return_value=rag):
            response = self.client.post(
                reverse("home"),
                {"body": "Anything?"},
                HTTP_HX_REQUEST="true",
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            GroupMessage.objects.filter(
                body__contains="Check that Ollama is running"
            ).exists()
        )


class LocalRagManifestTests(TestCase):
    def test_manifest_tracks_supported_file_changes(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "knowledge"
            markdown_dir = root / "markdown"
            storage_dir = root / "storage"
            source_dir.mkdir()
            (source_dir / "notes.md").write_text("Known fact", encoding="utf-8")
            (source_dir / "ignored.bin").write_text("ignored", encoding="utf-8")

            rag = LocalRag(
                source_dir=source_dir,
                markdown_dir=markdown_dir,
                storage_dir=storage_dir,
            )

            with patch.object(rag, "_build_and_persist_index", return_value=1):
                result = rag.rebuild_index()

            self.assertEqual(result["source_files"], 1)
            self.assertEqual(result["markdown_files"], 1)
            self.assertTrue((markdown_dir / "notes.md").exists())
            self.assertTrue(rag.manifest_path.exists())
            self.assertFalse(rag.index_is_current())

            rag.index_dir.mkdir(parents=True)
            self.assertTrue(rag.index_is_current())

            (source_dir / "notes.md").write_text("Known changed fact", encoding="utf-8")
            self.assertFalse(rag.index_is_current())

    def test_non_markdown_sources_are_converted_before_indexing(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "knowledge"
            markdown_dir = root / "markdown"
            storage_dir = root / "storage"
            source_dir.mkdir()
            (source_dir / "report.pdf").write_text("fake pdf", encoding="utf-8")

            rag = LocalRag(
                source_dir=source_dir,
                markdown_dir=markdown_dir,
                storage_dir=storage_dir,
            )

            converter = Mock()
            converter.convert.return_value = Mock(text_content="# Converted report")

            with patch("markitdown.MarkItDown", return_value=converter):
                with patch.object(rag, "_build_and_persist_index", return_value=1) as build:
                    result = rag.rebuild_index()

            converted_path = markdown_dir / "report.pdf.md"
            self.assertEqual(result["source_files"], 1)
            self.assertEqual(result["markdown_files"], 1)
            self.assertEqual(converted_path.read_text(encoding="utf-8"), "# Converted report")
            build.assert_called_once_with([converted_path])

    def test_extract_sources_deduplicates_file_names(self):
        rag = LocalRag(
            source_dir=Path("knowledge"),
            markdown_dir=Path("markdown"),
            storage_dir=Path("storage"),
        )
        response = Mock()
        response.source_nodes = [
            Mock(node=Mock(metadata={"file_name": "notes.md"})),
            Mock(node=Mock(metadata={"file_path": "/tmp/notes.md"})),
            Mock(node=Mock(metadata={"file_name": "budget.xlsx.md"})),
        ]

        self.assertEqual(rag._extract_sources(response), ("notes.md", "budget.xlsx"))


class RebuildRagIndexCommandTests(TestCase):
    def test_empty_knowledge_base_exits_clearly(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "knowledge"
            markdown_dir = root / "markdown"
            storage_dir = root / "storage"

            with override_settings(
                RAG_SOURCE_DIR=source_dir,
                RAG_MARKDOWN_DIR=markdown_dir,
                RAG_STORAGE_DIR=storage_dir,
            ):
                with self.assertRaises(CommandError) as raised:
                    call_command("rebuild_rag_index")

            self.assertIn("No supported files found", str(raised.exception))

    def test_rebuild_command_reports_success(self):
        rag = Mock()
        rag.rebuild_index.return_value = {
            "rebuilt": True,
            "source_files": 2,
            "markdown_files": 2,
            "documents": 3,
        }

        with patch("a_rtchat.management.commands.rebuild_rag_index.LocalRag.from_settings", return_value=rag):
            call_command("rebuild_rag_index")

        rag.rebuild_index.assert_called_once_with(force=True)
