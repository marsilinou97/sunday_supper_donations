"""
This script will populate the database with some default values that are needed
for basic functionality of the website. Most notable are the Anonymous Donor,
the enumerated types for clothing and funds, the user roles, and the default
user account.

The default user account is given the Admin role by default. The password should
be changed as soon as possible.
"""
from input.models import *
from settings.queries import update_user_role, activate_user
from django.contrib.auth.models import Group, User

def main():
    businesses = ("Trader Joe's", "Subway", "Walgreen's", "Papa John's", "El Pollo Loco", "Rite Aid")
    clothingTypes = ("Children's", "Men's", "Women's")
    fundTypes = ("Cash", "Check", "Electronic")
    groups = ("User", "Auditor", "Admin", "Superuser")

    # Insert the Anonymous Donor
    try:
        print("Inserting Anonymous Donor...")
        anonymous = InsertDonor("ANONYMOUS","ANONYMOUS","","","","","","","","")
        if anonymous != None:
            print("Successfully inserted Anonymous Donor")
        else:
            print("Could not insert Anonymous Donor")
    except Exception as e:
        print(e)

    # Insert some local businesses; this isn't comprehensive
    print("Inserting businesses...")
    count = 0
    for biz in businesses:
        try:
            curr = Business()
            curr.update(biz)
            curr.save()
            count += 1
        except Exception as e:
            print("Could not insert business", biz)
            print(e)
    print("Inserted", count, "businesses")

    # Insert some clothing types.
    print("Inserting clothing types...")
    count = 0
    for ct in clothingTypes:
        try:
            curr = ClothingType()
            curr.update(ct)
            curr.save()
            count += 1
        except Exception as e:
            print("Could not insert clothing type", ct)
            print(e)
    print("Inserted", count, "clothing types")

    # Insert some fund types.
    print("Inserting fund types...")
    count = 0
    for ft in fundTypes:
        try:
            curr = ClothingType()
            curr.update(ft)
            curr.save()
            count += 1
        except Exception as e:
            print("Could not insert fund type", ft)
            print(e)
    print("Inserted", count, "fund types")

    # Create the default groups.
    print("Inserting groups...")
    count = 0
    for g in groups:
        try:
            curr = Group()
            curr.name = g
            curr.save()
            count += 1
        except Exception as e:
            print("Could not insert groups", g)
            print(e)
    print("Inserted", count, "groups")

    # Create the default user.
    user = User()
    user.username = "director"
    user.is_active = True
    user.password = ""
    user.save()
    update_user_role(user.id, "Admin")
# End main

if __name__ == "__main__":
    main()
