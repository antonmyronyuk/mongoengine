from mongoengine import *

from config import CONFIG

connect(CONFIG['DB_NAME'])


class User(Document):  # collection
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

    meta = {'collection': 'users'}  # collection name in db

    # additional methods for representation collection
    # instance in print statements
    def __str__(self):
        return (
            '<User: first_name={}, last_name={}>'
        ).format(self.first_name, self.last_name)

    def __repr__(self):
        return self.__str__()


User.objects.delete()  # drop collection

User.objects.insert([  # bulk create users
    User(first_name='Ross', last_name='Geller'),
    User(first_name='Rachel', last_name='Green'),
    User(first_name='Monica', last_name='Geller'),
    User(first_name='Joey', last_name='Tribbiani'),
    User(first_name='Chandler', last_name='Bing'),
    User(first_name='Phoebe', last_name='Buffay'),
])

# QUERIES
print(User.objects)  # get all users

# get only users with last_name Geller or Green
print(User.objects(last_name__startswith='G'))

# add new user
new_user = User(first_name='Pavel', last_name='Kravets')
new_user.save()  # or User.objects.insert(new_user)
print(User.objects)

# update users
User.objects(first_name='Pavel').update(first_name='Julio', last_name='Cesar')
print(User.objects)

# update single user
try:
    user_to_update = User.objects.get(first_name='Monica')
except User.DoesNotExist:
    print('Oops, user does not exist')
else:
    user_to_update.first_name = 'Dominika'
    user_to_update.save()
finally:
    print(User.objects)

# delete user
print(User.objects(last_name='Bing').delete())  # number of users deleted
print(User.objects)

# objects count
print(User.objects.count())
