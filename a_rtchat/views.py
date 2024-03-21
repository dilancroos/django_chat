from django.shortcuts import render


def chat_view(request):
    return render(request, 'a_rtchat/chat.html')
