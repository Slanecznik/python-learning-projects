from users import users_list


# ========= УНИВЕРСАЛЬНЫЙ ПОИСК =========

def find_by(field, value):

    for user in users_list:

        if user[field].lower() == value.lower():

            return user

    return None


# ========= ПОИСК ПО ИМЕНИ =========

def find_user(name):
    return find_by("name", name)


# ========= ПОИСК ПО ГОРОДУ =========

def find_city(city):
    return find_by("city", city)


# ========= ПОИСК ПО ПРОФЕССИИ =========

def find_job(job):
    return find_by("job", job)