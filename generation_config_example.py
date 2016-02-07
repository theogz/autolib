from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config_example.ini')
config.add_section('main')
config.set('main', 'username', 'gmail.login')
config.set('main', 'password', 'correcthorsebatterystaple')
config.set('main', 'receiver', 'your.own.adresse@provider.com')

with open('config_example.ini', 'w') as f:
    config.write(f)