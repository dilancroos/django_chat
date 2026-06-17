from django.core.management.base import BaseCommand, CommandError

from a_rtchat.rag import KnowledgeBaseEmpty, LocalRag, LocalRagConfigurationError, LocalRagError


class Command(BaseCommand):
    help = "Build or refresh the local RAG index from the knowledge_base folder."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-unchanged",
            action="store_true",
            help="Do not rebuild when the stored manifest matches the knowledge folder.",
        )

    def handle(self, *args, **options):
        rag = LocalRag.from_settings()
        try:
            result = rag.rebuild_index(force=not options["skip_unchanged"])
        except KnowledgeBaseEmpty as exc:
            raise CommandError(str(exc)) from exc
        except LocalRagConfigurationError as exc:
            raise CommandError(str(exc)) from exc
        except LocalRagError as exc:
            raise CommandError(f"Could not rebuild the local RAG index: {exc}") from exc

        if result["rebuilt"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Converted {result['source_files']} source files into "
                    f"{result['markdown_files']} Markdown files and rebuilt the RAG index "
                    f"and {result['documents']} document chunks."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"RAG index is already current for {result['source_files']} source files "
                    f"and {result['markdown_files']} Markdown files."
                )
            )
