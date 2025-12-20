import random

class Generator:
    def generate_random_os(self):
        os_choices = [
            "Windows NT", "Macintosh; Intel Mac OS X", "Linux; U;", "X11; Ubuntu;"
        ]
        os = random.choice(os_choices)
        
        if os == "Windows NT":
            version = f"{random.randint(5, 10)}.{random.randint(0, 9)}.{random.randint(0, 9)}; Win{random.choice(['64', '32'])}; x64"
        elif os == "Macintosh; Intel Mac OS X":
            version = f"10_{random.randint(5, 15)}_{random.randint(0, 9)}"
        elif os == "Linux; U;":
            version = f"Linux {random.choice(['x86_64', 'i686'])}"
        elif os == "X11; Ubuntu;":
            version = f"Linux x86_64"
        elif os == "Android":
            version = f"{random.randint(4, 12)}.{random.randint(0, 9)}"
        elif os == "iPhone; CPU iPhone OS":
            version = f"{random.randint(10, 15)}_{random.randint(0, 9)}_{random.randint(0, 9)} like Mac OS X"
        return f"{os} {version}"

    # Function to generate a random browser version
    def generate_random_browser(self):
        browser_choices = ["Chrome", "Firefox", "Safari", "Edge", "Opera", "SamsungBrowser", "UC Browser", "Vivaldi"]
        browser = random.choice(browser_choices)
        
        if browser in ["Chrome", "Edge", "Opera"]:
            version = f"{random.randint(80, 100)}.{random.randint(0, 500)}.{random.randint(0, 5000)}.{random.randint(0, 100)}"
        elif browser == "Firefox":
            version = f"{random.randint(80, 100)}.0"
        elif browser == "Safari":
            version = f"{random.randint(600, 650)}.{random.randint(0, 10)}"
        elif browser == "SamsungBrowser":
            version = f"{random.randint(13, 14)}.{random.randint(0, 10)}"
        elif browser == "UC Browser":
            version = f"{random.randint(12, 15)}.{random.randint(0, 100)}"
        elif browser == "Vivaldi":
            version = f"{random.randint(4, 6)}.{random.randint(0, 10)}"
        return f"{browser}/{version}"

    # Function to generate a random WebKit version
    def generate_random_webkit(self):
        webkit_choices = ["AppleWebKit", "Gecko", "KHTML"]
        webkit = random.choice(webkit_choices)
        
        if webkit == "AppleWebKit":
            version = f"{random.randint(530, 550)}.{random.randint(0, 10)}"
        elif webkit == "Gecko":
            version = "20100101"
        elif webkit == "KHTML":
            version = f"like Gecko"
        
        return f"{webkit}/{version}"

    # Function to generate a truly random User-Agent string
    def generate(self):
        os = self.generate_random_os()
        browser = self.generate_random_browser()
        webkit = self.generate_random_webkit()
        
        user_agent = f"Mozilla/5.0 ({os}) {webkit} {browser} Safari/537.36"
        
        return user_agent


