import random
import string

class Utils:

    @staticmethod
    def generate_random_email(domains=None, tlds=None):
        if domains is None:
            domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
        if tlds is None:
            tlds = ["com", "net", "org", "co.uk"]
        
            username_length = random.randint(4, 15)
            username_characters = string.ascii_lowercase + string.digits
            username = ''.join(random.choice(username_characters) for _ in range(username_length))
            
            domain = random.choice(domains)
            tld = random.choice(tlds)
        
        return f"{username}@{domain}.{tld}"