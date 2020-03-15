from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import requests
import threading
# Create your views here.
from datetime import datetime
import time
import json


def get_dict_from_POST(post) -> dict:
    json_string = list(post.keys())[0]
    return json.loads(json_string)


def only_super_user_is_allowed(request: HttpRequest):
    return JsonResponse({
        'msg': 'Only superuser is allowed.'
    }, status=400)


def get_and_set_cookie(request: HttpRequest):
    print(request.COOKIES)
    response = JsonResponse({
        'key': 'value',
    })
    response.set_cookie('datetime', str(datetime.now()))
    return response


def user_info(request: HttpRequest):
    user: User = request.user
    if request.user.is_authenticated:
        return JsonResponse({
            'hasLoggedIn': True,
            'username': user.username,
            'isSuperUser': user.is_superuser
        })
    else:
        return JsonResponse({
            'hasLoggedIn': False,
        })


@user_passes_test(test_func=lambda user: user.is_superuser, login_url='only_superuser_is_allowed')
def user_infos(request: HttpRequest):
    return JsonResponse({
        'userInfos': [
            {'username': user.username, 'id': user.id, 'isSuperUser': user.is_superuser} for user in User.objects.all()
        ]
    })


def log_in(request: HttpRequest):
    o = get_dict_from_POST(request.POST)
    username = o.get('username')
    password = o.get('password')
    user: User = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({
            'hasLoggedIn': True,
            'username': user.username,
        })
    else:
        return JsonResponse({
            'hasLoggedIn': False,
        })


def log_out(request: HttpRequest):
    user: User = request.user
    if not user.is_authenticated:
        return JsonResponse({
            'msg': 'Have not logged in.',
            'hasLoggedOut': True,
        }, status=400)
    logout(request)
    return JsonResponse({
        'msg': 'You have logged out.',
        'hasLoggedOut': True,
    })


@user_passes_test(test_func=lambda user: user.is_superuser, login_url='only_superuser_is_allowed')
def register(request: HttpRequest):
    o = get_dict_from_POST(request.POST)
    username = o.get('username')

    password = o.get('password')
    register_as_super_user = o.get('registerAsSuperUser')
    if User.objects.filter(username=username):
        return JsonResponse({
            'msg': 'The name is occupied,try another',
            'userNameExists': True,
        })
    if register_as_super_user:
        user: User = User.objects.create_superuser(
            username=username, password=password)
    else:
        user: User = User.objects.create_user(
            username=username, password=password)
    user.save()
    return JsonResponse({
        'msg': 'User added.',
        'username': user.username,
        'isUserAdded': True,
    })


def delete_user(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({
            'msg': 'Only POST is allowed.'
        }, status=400)
    d = get_dict_from_POST(request.POST)
    _id = d.get('idOfUserToDelete')
    user: User = User.objects.filter(id=_id)
    if user:
        user.delete()
        return JsonResponse({
            'idOfDeletedUser': _id,
            'deleted': True,
        })
    else:
        return JsonResponse({
            'msg': 'Failed.'
        })


def get_data(request: HttpRequest):
    time.sleep(0.15)
    return JsonResponse({
        'dateTime': str(datetime.now())+'?'
    })
