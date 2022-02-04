import json

from database.backend_database import get_all_users_with_id, _delete_all_users, set_users, update_user, get_all_users

users = get_all_users_with_id()
# [
#   {
#     "_id": "l@gmail.com",
#     "user_details": {
#       "username": "Logeshh",
#       "password": "password",
#       "mail_id": "l@gmail.com"
#     }
#   },
#   {
#     "_id": "Logesh_@gmail.com",
#     "user_details": {
#       "username": "Logesh",
#       "password": "string",
#       "mail_id": "Logesh_@gmail.com"
#     }
#   }
# ]

print(json.dumps(users, indent=2))
print('')

set_users(
                        {'username': 'Log',
                        'password': 'Logesh password',
                        'mail_id': 'l@gmail.com'
                        })

update_user({'password': 'password', 'mail_id': 'l@gmail.com'})
users = get_all_users()
print(json.dumps(users, indent=2))
print('')

_delete_all_users()