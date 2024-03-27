from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatmessageCreateForm
from sel import get_data

import os
from llamaapi import LlamaAPI
from dotenv import load_dotenv

load_dotenv()


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="ai-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    # context = {}

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            # Initialize the SDK
            # get the key from the .env file
            llama_api_key = os.getenv("LLAMA_API_KEY")

            llama = LlamaAPI(llama_api_key)

            # msg.append(message.body)
            try:
                data = get_data(message.body)
            except:
                print("error")

            # Build the API request
            api_request_json = {
                "messages": [
                    {"role": "user", "content": message.body},
                ],
                "stream": False,
            }

            # Execute the Request
            response = llama.run(api_request_json)

            # get the response
            response = llama.run(api_request_json).json()[
                "choices"][0]["message"]["content"]
            print(response)

            # initialize the message
            message2 = GroupMessage()
            message2.body = response
            message2.author = User.objects.get(username="botty")
            message2.group = chat_group
            message2.save()
            context = {
                'message': message,
                'user': request.user,
                'message2': message2,
                'user2': User.objects.get(username="botty")
            }

            # write the message2 to the txt file
            with open("./data/data.txt", "a") as file:
                file.write(f"{message2.body}\n")

            return render(request, 'a_rtchat/partials/chat_messages_p.html', context)

    return render(request, 'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form': form})
