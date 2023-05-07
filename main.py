# Start file

from client import WarnBirdClientConfig, WarnBirdClient


# Parse args to create client with

# cfg = WarnbirdClientConfig.from_args(None) # from command line args

client = WarnBirdClient(None)

client.start()
