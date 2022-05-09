from pyexpat import model
from django.contrib.postgres.fields import ArrayField
from django import forms
from django.forms import CharField
from djongo import models
from django.db import models as djmodels
from django.contrib.auth import get_user_model
from djongo.models import Q 
from django.contrib.auth.models import User
from zmq import NULL

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct() 
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    is_first_msg = models.BooleanField(name='is_first_msg', default=True)
    
    first_person_send = models.BooleanField(name='first_person_send', default=False)
    second_person_send = models.BooleanField(name='second_person_send', default=False)
    
    first_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='first_sender')    

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
 
   
# class FriendList(models.Model):
#     self = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='self_user_id')
#     friend = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='friend_id')
#     friend_username = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)