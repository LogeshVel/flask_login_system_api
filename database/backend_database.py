import json

import pymongo

from database.mongo_db_details import Users  # import this from the root folder for FLASK to understand.

client = pymongo.MongoClient(Users().SERVER_URI)
db = client[Users().DATABASE_NAME]
db_collection = db[Users().COLLECTION_NAME]

ALL_USERS_LIST = []


def remove_id(mongo_db_result_dict):
    """
    :param mongo_db_result_dict: individual posts in the DB
    :return: dict removed with the Mongo DB id for each posts
    """
    return {k: v for k, v in mongo_db_result_dict.items() if not k.startswith("_")}


def get_all_users():
    result = db_collection.find()
    all_users_list = []
    for r in result:
        all_users_list.append(remove_id(r))
    # print(all_users_list)
    return all_users_list


def get_all_users_with_id():
    result = db_collection.find()
    all_users_list = []
    for r in result:
        all_users_list.append(r)
    return all_users_list


def set_users(user_dict):
    """
    :param user_dict:
                        {'username': 'Log',
                        'password': 'Logesh password',
                        'mail_id': 'l@gmail.com'
                        }
    :return:
    """
    try:
        if "username" not in user_dict or "password" not in user_dict or "mail_id" not in user_dict:
            return False
        mail = str(user_dict['mail_id'])
        uname = str(user_dict["username"])
        password = str(user_dict["password"])
        user_data = {"username": uname, "password": password, "mail_id": mail}
        db_collection.insert_one({"_id": mail, "user_details": user_data})
        return True
    except Exception as e:
        print(e)
        return False


def _delete_all_users():
    r = db_collection.delete_many({})
    print("Total item deleted from the Devices Mongo db before strting the application is : ", r.deleted_count)


def check_email_exist(mail_id):
    users_list = get_all_users_with_id()
    for user in users_list:
        if mail_id.lower() == user['_id'].lower():
            return {"status": True, "description": "mail_id exists"}
    return {"status": False, "description": "mail_id not exists"}


def check_email_exists_from_all_users(all_user_list, mail_id):
    """
    :param all_user_list: must conatins the _id key
    :param mail_id:
    :return:
    """
    for user in all_user_list:
        if mail_id.lower() == user['_id'].lower():
            return {"status": True, "description": "mail_id exists"}
    return {"status": False, "description": "mail_id not exists"}


def get_username_from_user_lists(all_user_list, mail_id):
    """
    :param all_user_list: must conatins the _id key
    :param mail_id:
    :return:
    """
    for user in all_user_list:
        if mail_id.lower() in user['_id'].lower():
            return str(user["user_details"]["username"])
    return None


def update_user(user_dict={}):
    """
    Used for forget password feature
    :param user_dict: {
                        "new_password": "pass",
                        "mail_id": "mailid"
                        }
    :return:
    """
    if user_dict == {}:
        return False

    users_list = get_all_users_with_id()
    chk = check_email_exists_from_all_users(users_list, str(user_dict['mail_id']))
    print(chk)
    password = str(user_dict["new_password"])
    mail = str(user_dict["mail_id"])

    user_data = {"username": get_username_from_user_lists(users_list, mail),
                 "password": password,
                 "mail_id": mail}
    if chk["status"]:
        filter_to_update = {"_id": mail}
        to_update = {"$set": {"user_details": user_data}}
        db_collection.update_one(filter_to_update, to_update)
        return True

    return False


def validate_user(user_data):
    """
    :param user_data: {
                        "password": "pass",
                        "mail_id": "mailid"
                        }
    :return:
    """
    given_mail = str(user_data['mail_id'])
    given_password = str(user_data['password'])

    users_list = get_all_users_with_id()
    for user in users_list:
        if given_mail.lower() == user['_id'].lower():
            if user['user_details']['mail_id'].lower() == given_mail.lower() and user['user_details']['password'] == str(given_password):
                return True
    return False


