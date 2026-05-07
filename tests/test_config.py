from config.environment import config

def test_config():
    print(config["base_url"])
    print(config["credentials"]["username"])