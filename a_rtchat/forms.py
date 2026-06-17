from django.forms import ModelForm
from django import forms
from .models import *


class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Type a message...',
                'class': 'min-h-[3.25rem] max-h-32 flex-1 resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm leading-6 text-slate-100 placeholder:text-slate-500 outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-400/20',
                'maxlength': '2000',
                'rows': '2',
                'autofocus': True,
            }),
        }
