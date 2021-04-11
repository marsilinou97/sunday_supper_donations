from input.models import *
from users.models import *
from django.db.models import F
from django.contrib.auth.models import Group, User

def get_users_info():
    return User.objects.annotate(role=F('groups__name')).values('id','username', 'email', 'role', 'is_active')

def get_all_roles():
    return Group.objects.annotate(role=F('name')).values('role')

def update_user_role(id: int, role: str):
    user = User.objects.get(id=id)
    user.groups.clear()
    
    new_role = Group.objects.get(name=role)
    new_role.user_set.add(user)

def activate_user(id: int, active: bool):
    user = User.objects.get(id=id)
    user.is_active = active
    user.save()

def test_code():
    group = Group.objects.get(name="test_group")
    group2 = Group.objects.get(name="test_group2")
    user_to_add = User.objects.get(username="brad")
    user_to_add.groups.clear()
    group.user_set.add(user_to_add)
    group2.user_set.add(user_to_add)