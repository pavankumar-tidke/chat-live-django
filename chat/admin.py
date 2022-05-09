
from django.contrib import admin 
from djongo.models import Q
from .models import Thread, ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
 

admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage
 
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)


# admin.site.register(FriendList)


