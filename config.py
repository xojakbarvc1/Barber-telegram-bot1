from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
ADMIN = env.int("ADMIN")
CHANNEL_ID = env.int("CHANNEL_ID")