import random
import string

def generate_random_company_name():
    """Generate a random company name in the format: [E2E] Playwright{random digit}"""
    random_digit = random.randint(1, 9999)
    random_char = random.choice(string.ascii_uppercase)
    return f"Playwright_{random_digit}:{random_char}"

def generate_random_email():
    """Generate a random email address in the format: [E2E] Playwright{random digit}@example.com"""
    random_digit = random.randint(1, 9999)
    random_char = random.choice(string.ascii_lowercase)
    return f"playwright.{random_digit}{random_char}@example.com"


def generate_valid_password():
    """Generate a random password that meets all requirements:
    - At least 8 characters
    - Contains lowercase
    - Contains uppercase
    - Contains numbers
    - Contains special characters
    """
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Add additional random characters to meet minimum length
    remaining_length = random.randint(4, 8)  # Add 4-8 more characters
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def generate_invalid_password():
    """Generate a random invalid password that fails one or more requirements"""
    invalid_types = [
        "no_lowercase",
        "no_uppercase",
        #"no_numbers",       
        "too_short",
        "all_lowercase",
        "all_uppercase",
        "all_numbers",
        "all_special"
    ]
    
    invalid_type = random.choice(invalid_types)
    
    if invalid_type == "no_lowercase":
        return ''.join(random.choices(string.ascii_uppercase + string.digits + "!@#$%^&*", k=random.randint(8, 12)))
    elif invalid_type == "no_uppercase":
        return ''.join(random.choices(string.ascii_lowercase + string.digits + "!@#$%^&*", k=random.randint(8, 12)))
    #elif invalid_type == "no_numbers":
        return ''.join(random.choices(string.ascii_letters + "!@#$%^&*", k=random.randint(8, 12)))    
    elif invalid_type == "too_short":
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=random.randint(4, 7)))
    elif invalid_type == "all_lowercase":
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 12)))
    elif invalid_type == "all_uppercase":
        return ''.join(random.choices(string.ascii_uppercase, k=random.randint(8, 12)))
    elif invalid_type == "all_numbers":
        return ''.join(random.choices(string.digits, k=random.randint(8, 12)))
    elif invalid_type == "all_special":
        return ''.join(random.choices("!@#$%^&*()_+-=[]{}|;:,.<>?", k=random.randint(8, 12)))

# Test passwords for validation
PASSWORD_TEST_CASES = {
    "valid": generate_valid_password(),  # Random valid password
    "no_lowercase": "TEST123!@#",  # Missing lowercase
    "no_uppercase": "test123!@#",  # Missing uppercase
    "too_short": "Test1!",  # Less than 8 characters
    #"no_numbers": "Test!@#$",  # No numbers
    "all_lowercase": "testtest",  # All lowercase
    "all_uppercase": "TESTTEST",  # All uppercase
    "all_numbers": "12345678",  # All numbers
    "all_special": "!@#$%^&*",  # All special characters
    "random_invalid_1": generate_invalid_password(),  # Random invalid password
    "random_invalid_2": generate_invalid_password(),  # Another random invalid password
    "random_invalid_3": generate_invalid_password(),  # Another random invalid password
}

userData = [
    {

        "first_name": "Sherill",
        "last_name": "Swanborrow[Playwright]",
        "email": "sswanborrow2@nationalgeographic.com",
        "gender": "Female",
        "password": "P1lMfd8Jt",
        "confirm_password": "P1lMfd8Jt", 
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Sherill Swanborrow"
    },
    {

        "first_name": "Simona",
        "last_name": "Thring[Playwright]",
        "email": "sthring3@a8.net",
        "gender": "Female",
        "password": "Simona0B1r1pI",
        "confirm_password": "Simona0B1r1pI",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Simona Thring"
    },
    {

        "first_name": "Bartholemy",
        "last_name": "Osselton[Playwright]",
        "email": "bosselton4@hubpages.com",
        "gender": "Male",
        "password": "3PYaY1",
        "confirm_password": "3PYaY1",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Bartholemy Osselton"
    },
    {

        "first_name": "Tripp",
        "last_name": "Bigrigg[Playwright]",
        "email": "tbigrigg5@drupal.org",
        "gender": "Male",
        "password": "IycpEnadmm",
        "confirm_password": "IycpEnadmm",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Tripp Bigrigg"
    },
    {
        "first_name": "Ross",
        "last_name": "Bagott[Playwright]",
        "email": "rbagott6@msn.com",
        "gender": "Male",
        "password": "NnY7w9aMg",
        "confirm_password": "NnY7w9aMg",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Ross Bagott"
    },
    {

        "first_name": "Alexia",
        "last_name": "Lince[Playwright]",
        "email": "alince7@hugedomains.com",
        "gender": "Female",
        "password": "B5Ijp6o",
        "confirm_password": "B5Ijp6o",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Alexia Lince"
    },
    {

        "first_name": "Yorker",
        "last_name": "Kiffe[Playwright]",
        "email": "ykiffe8@imageshack.us",
        "gender": "Genderfluid",
        "password": "tOYhbcY",
        "confirm_password": "tOYhbcY",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Yorker Kiffe"
    },
    {

        "first_name": "Sylas",
        "last_name": "Crickmore[Playwright]",
        "email": "scrickmore9@yellowbook.com",
        "gender": "Male",
        "password": "uyek7BUT",
        "confirm_password": "uyek7BUT",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Sylas Crickmore"
    },
    {

        "first_name": "Marthena",
        "last_name": "Ginnally[Playwright]",
        "email": "mginnallya@cdbaby.com",
        "gender": "Female",
        "password": "dS5xmFZk",
        "confirm_password": "dS5xmFZk",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Marthena Ginnally"
    },
    {

        "first_name": "Shir",
        "last_name": "Brandoni[Playwright]",
        "email": "sbrandonib@csmonitor.com",
        "gender": "Female",
        "password": "25UvIeV",
        "confirm_password": "25UvIeV",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Shir Brandoni"
    },
    {

        "first_name": "Wells",
        "last_name": "Hursey[Playwright]",
        "email": "whurseyc@ustream.tv",
        "gender": "Male",
        "password": "eo0ygmqgYc",
        "confirm_password": "eo0ygmqgYc",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Wells Hursey"
    },
    {

        "first_name": "Zacharia",
        "last_name": "Garrould[Playwright]",
        "email": "zgarrouldd@usa.gov",
        "gender": "Male",
        "password": "370KcO",
        "confirm_password": "370KcO",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Zacharia Garrould"
    },
    {
        "first_name": "Drona",
        "last_name": "Kinsett[Playwright]",
        "email": "dkinsette@amazon.de",
        "gender": "Female",
        "password": "76aSZIp3vw6u",
        "confirm_password": "76aSZIp3vw6u",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Drona Kinsett"
    },
    {
        "first_name": "Eunice",
        "last_name": "Camelin[Playwright]",
        "email": "ecamelinf@youtube.com",
        "gender": "Female",
        "password": "0Sy55ffLSY",
        "confirm_password": "0Sy55ffLSY",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Eunice Camelin"
    },
    {
        "first_name": "Loleta",
        "last_name": "Fearnsides[Playwright]",
        "email": "lfearnsidesg@ask.com",
        "gender": "Female",
        "password": "zdNHfouCfZf",
        "confirm_password": "zdNHfouCfZf",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Loleta Fearnsides"
    },
    {
        "first_name": "Pace",
        "last_name": "Paulmann[Playwright]",
        "email": "ppaulmannh@sciencedaily.com",
        "gender": "Male",
        "password": "bMIUj8",
        "confirm_password": "bMIUj8",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Pace Paulmann"
    },
    {
        "first_name": "Clair",
        "last_name": "Finby[Playwright]",
        "email": "cfinbyi@gmpg.org",
        "gender": "Female",
        "password": "l7Qw5nP9rDbZ",
        "confirm_password": "l7Qw5nP9rDbZ",
        "company_name": "Playwright-Corporate Kft.",
        "user_name": "Clair Finby"
    }
]

# Update all user passwords to be valid
for user in userData:
    user["password"] = generate_valid_password()
    user["confirm_password"] = user["password"]

def get_random_user():
    """Get a random user from the userData list and update company name"""
    user = random.choice(userData)
    user["company_name"] = generate_random_company_name()
    user["email"] = generate_random_email()
    return user


