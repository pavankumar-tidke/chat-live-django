from django.urls import path
from . import views
urlpatterns = [
    path('', views.messages_page),
    
    path('search_user', views.search_users),
    path('createnewthread', views.create_new_thread),
    path('checkfirstmsg', views.check_first_msg),
    path('updatefirstmsgstatus', views.update_first_status)
    
]
 