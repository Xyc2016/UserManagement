from django.urls import path
from . import views
urlpatterns = [
    path('get_and_set_cookie', views.get_and_set_cookie, name='get_and_set_cookie'),
    path('log_in', views.log_in, name='log_in'),
    path('user_info', views.user_info, name='user_info'),
    path('register', views.register, name='register'),
    path('log_out', views.log_out, name='log_out'),
    path('user_infos', views.user_infos,
         name='user_infos'),
    path('only_superuser_is_allowed', views.only_super_user_is_allowed,
         name='only_superuser_is_allowed'),
    path('delete_user', views.delete_user, name='delete_user')
]
