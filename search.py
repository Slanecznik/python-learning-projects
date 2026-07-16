from users_backup import users_list


# ========= УНИВЕРСАЛЬНЫЙ ПОИСК =========

def find_by(field, value):

    for user in users_list:

        if user[field].lower() == value.lower():

            return user

    return None

# ========= УНИВЕРСАЛЬНЫЙ СЧЁТЧИК =========

def count_by(field):

    counter = {}

    for user in users_list:

        value = user[field]

        if value in counter:

            counter[value] += 1

        else:

            counter[value] = 1

    return counter

# ========= ПОИСК ПО ИМЕНИ =========

def find_user(name):
    return find_by("name", name)


# ========= ПОИСК ПО ГОРОДУ =========

def find_city(city):
    return find_by("city", city)


# ========= ПОИСК ПО ПРОФЕССИИ =========

def find_job(job):
    return find_by("job", job)

# ========= СОЗДАНИЕ СООБЩЕНИЯ =========

def make_stats_message(title, data):

    message = f"{title}\n\n"

    for key in data:

        message += f"{key}: {data[key]}\n"

    return message