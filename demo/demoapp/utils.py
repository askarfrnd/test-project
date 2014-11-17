import random
import string
from django.contrib.auth.models import User


def create_random_string():
    random_string = random.choice(string.ascii_lowercase)
    while True:
        random_string += ''.join(random.choice(string.digits) for x in range(6))
        check_random_string = User.objects.filter(username__iexact=random_string)
        if check_random_string.count() == 0:
            break
    return random_string
