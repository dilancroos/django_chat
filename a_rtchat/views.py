from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import ChatmessageCreateForm
from .models import ChatGroup, GroupMessage
from .rag import KnowledgeBaseEmpty, LocalRag, LocalRagConfigurationError, LocalRagError


CHAT_GROUP_NAME = "ai-chat"
BOT_USERNAME = "botty"


@login_required
def chat_view(request):
    chat_group = _get_chat_group()
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            message2 = _create_bot_message(chat_group, message.body)
            context = {
                "message": message,
                "message2": message2,
                "user": request.user,
            }
            if request.htmx:
                return render(request, "a_rtchat/partials/chat_messages_p.html", context)
            return redirect("home")

    return render(request, "a_rtchat/chat.html", {"chat_messages": chat_messages, "form": form})


def _get_chat_group() -> ChatGroup:
    chat_group, _created = ChatGroup.objects.get_or_create(group_name=CHAT_GROUP_NAME)
    return chat_group


def _get_bot_user() -> User:
    bot_user, created = User.objects.get_or_create(
        username=BOT_USERNAME,
        defaults={"email": "botty@example.local", "is_active": False},
    )
    if created:
        bot_user.set_unusable_password()
        bot_user.save(update_fields=["password"])
    return bot_user


def _create_bot_message(chat_group: ChatGroup, question: str) -> GroupMessage:
    body = _answer_question(question)
    return GroupMessage.objects.create(
        body=body,
        author=_get_bot_user(),
        group=chat_group,
    )


def _answer_question(question: str) -> str:
    try:
        answer = LocalRag.from_settings().answer(question)
    except KnowledgeBaseEmpty as exc:
        return str(exc)
    except LocalRagConfigurationError as exc:
        return str(exc)
    except LocalRagError:
        return (
            "I could not query the local knowledge base. "
            "Check that Ollama is running and the configured models are installed."
        )

    if not answer.sources:
        return answer.text

    sources = ", ".join(answer.sources)
    return f"{answer.text}\n\nSources: {sources}"
