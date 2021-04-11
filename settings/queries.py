from input.models import *
from users.models import *
from django.db.models import F
from django.contrib.auth.models import Group, User

def get_users_info():
    return User.objects.annotate(role=F('groups__name')).values('id','username', 'email', 'role')

def get_all_roles():
    return Group.objects.annotate(role=F('name')).values('role')

def update_user_role(username: str, role: str):
    user = User.objects.get(username=username)
    user.groups.clear()
    
    new_role = Group.objects.get(name=role)
    status = new_role.user_set.add(user)
    return status


def test_code():
    group = Group.objects.get(name="test_group")
    user_to_add = User.objects.get(username="brad")
    user_to_add.groups.clear()
    group.user_set.add(user_to_add)