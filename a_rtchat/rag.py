from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)


class LocalRagError(Exception):
    """Base error for local RAG failures."""


class KnowledgeBaseEmpty(LocalRagError):
    """Raised when the knowledge folder has no readable files."""


class LocalRagConfigurationError(LocalRagError):
    """Raised when local RAG dependencies or settings are missing."""


@dataclass(frozen=True)
class RagAnswer:
    text: str
    sources: tuple[str, ...] = ()


class LocalRag:
    SOURCE_SUFFIXES = {
        ".csv",
        ".doc",
        ".docx",
        ".epub",
        ".htm",
        ".html",
        ".json",
        ".md",
        ".pdf",
        ".ppt",
        ".pptx",
        ".txt",
        ".xls",
        ".xlsx",
        ".xml",
        ".zip",
    }
    MANIFEST_VERSION = 2

    def __init__(
        self,
        source_dir: Path,
        markdown_dir: Path,
        storage_dir: Path,
        *,
        ollama_base_url: str = "http://localhost:11434",
        chat_model: str = "llama3.2",
        embed_model: str = "nomic-embed-text",
        similarity_top_k: int = 4,
        request_timeout: float = 120.0,
    ) -> None:
        self.source_dir = Path(source_dir)
        self.markdown_dir = Path(markdown_dir)
        self.storage_dir = Path(storage_dir)
        self.index_dir = self.storage_dir / "index"
        self.manifest_path = self.storage_dir / "manifest.json"
        self.ollama_base_url = ollama_base_url
        self.chat_model = chat_model
        self.embed_model = embed_model
        self.similarity_top_k = similarity_top_k
        self.request_timeout = request_timeout

    @classmethod
    def from_settings(cls) -> "LocalRag":
        return cls(
            source_dir=Path(settings.RAG_SOURCE_DIR),
            markdown_dir=Path(settings.RAG_MARKDOWN_DIR),
            storage_dir=Path(settings.RAG_STORAGE_DIR),
            ollama_base_url=settings.OLLAMA_BASE_URL,
            chat_model=settings.OLLAMA_CHAT_MODEL,
            embed_model=settings.OLLAMA_EMBED_MODEL,
            similarity_top_k=settings.RAG_SIMILARITY_TOP_K,
            request_timeout=settings.OLLAMA_REQUEST_TIMEOUT,
        )

    def answer(self, question: str) -> RagAnswer:
        try:
            index = self._load_or_rebuild_index()
            query_engine = index.as_query_engine(similarity_top_k=self.similarity_top_k)
            response = query_engine.query(question)
        except LocalRagError:
            raise
        except ImportError as exc:
            raise LocalRagConfigurationError(
                "Local RAG dependencies are not installed. Run pip install -r requirements.txt."
            ) from exc
        except Exception as exc:
            raise LocalRagError(str(exc)) from exc

        return RagAnswer(text=str(response), sources=self._extract_sources(response))

    def rebuild_index(self, *, force: bool = True) -> dict[str, Any]:
        source_files = self._source_files()
        if not source_files:
            raise KnowledgeBaseEmpty(
                f"No supported files found in {self.source_dir}. "
                "Add PDF, Word, Excel, PowerPoint, Markdown, HTML, CSV, JSON, XML, ZIP, or TXT files."
            )

        manifest = self._current_manifest(source_files)
        if not force and self._stored_manifest() == manifest and self.index_dir.exists():
            return {
                "rebuilt": False,
                "source_files": len(source_files),
                "markdown_files": len(self._markdown_files()),
            }

        if self.index_dir.exists():
            shutil.rmtree(self.index_dir)

        markdown_files = self._convert_sources_to_markdown(source_files)
        documents_count = self._build_and_persist_index(markdown_files)
        self._write_manifest(manifest)
        return {
            "rebuilt": True,
            "source_files": len(source_files),
            "markdown_files": len(markdown_files),
            "documents": documents_count,
        }

    def index_is_current(self) -> bool:
        source_files = self._source_files()
        if not source_files or not self.index_dir.exists():
            return False
        return self._stored_manifest() == self._current_manifest(source_files)

    def _convert_sources_to_markdown(self, source_files: list[Path]) -> list[Path]:
        try:
            from markitdown import MarkItDown
        except ImportError as exc:
            raise LocalRagConfigurationError(
                "MarkItDown is not installed. Run pip install -r requirements.txt."
            ) from exc

        if self.markdown_dir.exists():
            shutil.rmtree(self.markdown_dir)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)

        converter = MarkItDown(enable_plugins=False)
        markdown_files: list[Path] = []
        for source_path in source_files:
            output_path = self._markdown_output_path(source_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            markdown_text = self._convert_source(source_path, converter)
            if not markdown_text.strip():
                logger.warning("Skipping empty converted Markdown file: %s", source_path)
                continue
            output_path.write_text(markdown_text, encoding="utf-8")
            markdown_files.append(output_path)

        if not markdown_files:
            raise KnowledgeBaseEmpty(
                f"Supported files were found in {self.source_dir}, but no Markdown content could be read."
            )

        return markdown_files

    def _convert_source(self, source_path: Path, converter: Any) -> str:
        if source_path.suffix.lower() == ".md":
            return source_path.read_text(encoding="utf-8")

        try:
            result = converter.convert(str(source_path))
        except Exception as exc:
            raise LocalRagError(f"Could not convert {source_path.name} to Markdown: {exc}") from exc

        return getattr(result, "text_content", None) or getattr(result, "markdown", "") or ""

    def _markdown_output_path(self, source_path: Path) -> Path:
        relative_path = source_path.relative_to(self.source_dir)
        if source_path.suffix.lower() == ".md":
            output_relative_path = relative_path
        else:
            output_relative_path = relative_path.with_name(f"{relative_path.name}.md")
        return self.markdown_dir / output_relative_path

    def _build_and_persist_index(self, markdown_files: list[Path]) -> int:
        try:
            self._configure_llama_index()
            from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
        except ImportError as exc:
            raise LocalRagConfigurationError(
                "Local RAG dependencies are not installed. Run pip install -r requirements.txt."
            ) from exc

        documents = SimpleDirectoryReader(input_files=[str(path) for path in markdown_files]).load_data()
        if not documents:
            raise KnowledgeBaseEmpty(
                f"Markdown files were created in {self.markdown_dir}, but no text could be read."
            )

        index = VectorStoreIndex.from_documents(documents)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        index.storage_context.persist(persist_dir=str(self.index_dir))
        return len(documents)

    def _load_or_rebuild_index(self) -> Any:
        if not self.index_is_current():
            self.rebuild_index(force=True)

        try:
            self._configure_llama_index()
            from llama_index.core import StorageContext, load_index_from_storage
        except ImportError as exc:
            raise LocalRagConfigurationError(
                "Local RAG dependencies are not installed. Run pip install -r requirements.txt."
            ) from exc

        storage_context = StorageContext.from_defaults(persist_dir=str(self.index_dir))
        return load_index_from_storage(storage_context)

    def _configure_llama_index(self) -> None:
        from llama_index.core import Settings
        from llama_index.embeddings.ollama import OllamaEmbedding
        from llama_index.llms.ollama import Ollama

        Settings.llm = Ollama(
            model=self.chat_model,
            base_url=self.ollama_base_url,
            request_timeout=self.request_timeout,
        )
        Settings.embed_model = OllamaEmbedding(
            model_name=self.embed_model,
            base_url=self.ollama_base_url,
        )

    def _source_files(self) -> list[Path]:
        self.source_dir.mkdir(parents=True, exist_ok=True)
        files: list[Path] = []

        for path in sorted(self.source_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.name.startswith("."):
                continue
            if path.suffix.lower() not in self.SOURCE_SUFFIXES:
                logger.warning("Skipping unsupported knowledge-base source file: %s", path)
                continue
            files.append(path)

        return files

    def _markdown_files(self) -> list[Path]:
        if not self.markdown_dir.exists():
            return []
        return sorted(path for path in self.markdown_dir.rglob("*.md") if path.is_file())

    def _current_manifest(self, source_files: list[Path]) -> dict[str, Any]:
        return {
            "version": self.MANIFEST_VERSION,
            "source_dir": str(self.source_dir),
            "markdown_dir": str(self.markdown_dir),
            "files": [
                {
                    "path": path.relative_to(self.source_dir).as_posix(),
                    "markdown_path": self._markdown_output_path(path)
                    .relative_to(self.markdown_dir)
                    .as_posix(),
                    "size": path.stat().st_size,
                    "mtime_ns": path.stat().st_mtime_ns,
                }
                for path in source_files
            ],
        }

    def _stored_manifest(self) -> dict[str, Any] | None:
        if not self.manifest_path.exists():
            return None
        try:
            return json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Ignoring invalid RAG manifest: %s", self.manifest_path)
            return None

    def _write_manifest(self, manifest: dict[str, Any]) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    def _extract_sources(self, response: Any) -> tuple[str, ...]:
        source_names: list[str] = []
        for source_node in getattr(response, "source_nodes", []) or []:
            node = getattr(source_node, "node", source_node)
            metadata = getattr(node, "metadata", {}) or {}
            source = metadata.get("file_name") or metadata.get("file_path")
            if not source:
                continue
            source_name = self._display_source_name(Path(str(source)).name)
            if source_name not in source_names:
                source_names.append(source_name)
        return tuple(source_names)

    def _display_source_name(self, markdown_name: str) -> str:
        if not markdown_name.endswith(".md"):
            return markdown_name

        original_name = markdown_name.removesuffix(".md")
        if Path(original_name).suffix:
            return original_name
        return markdown_name
