from input.models import *
from users.models import *
from django.db.models import F
from django.contrib.auth.models import Group, User

def get_users_info(offset: int, limit: int):
    users = User.objects.annotate(role=F('groups__name')).values('id','username', 'email', 'role', 'is_active')
    users = users[offset:offset + limit]
    return users

def get_all_roles():
    return Group.objects.annotate(role=F('name')).values('role')

def update_user_role(id: int, role: str):
    user = User.objects.get(id=id)
    user.groups.clear()

    new_role = Group.objects.get(name=role)
    new_role.user_set.add(user)

    if role == "Admin":
        user.is_staff = True
        user.is_superuser = False
    elif role == "Superuser":
        user.is_staff = True
        user.is_superuser = True
    else:
        user.is_staff = False
        user.is_superuser = False
    user.save()

def activate_user(id: int, active: bool):
    user = User.objects.get(id=id)
    user.is_active = active
    user.save()

def get_token_data(offset: int, limit: int):
    tokens = RegistrationToken.objects.select_related('user').annotate(creator_name=F('creator__username')).values()
    tokens = tokens[offset:offset + limit]
    return tokens

def update_token_data(token_id: int, data: dict):
    return RegistrationToken.objects.filter(id=token_id).update(**data)

def delete_token(token_id: int):
    try:
        token = RegistrationToken.objects.filter(id=token_id).delete()
        print("deletion results: ",token)
        return True
    except Exception as e:
        print(e)
        return False

def test_code():
    group = Group.objects.get(name="test_group")
    group2 = Group.objects.get(name="test_group2")
    user_to_add = User.objects.get(username="brad")
    user_to_add.groups.clear()
    group.user_set.add(user_to_add)
    group2.user_set.add(user_to_add)
