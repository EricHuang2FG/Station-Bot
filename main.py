from bot import runDiscordBot
from run import keepAlive
from RemoveFile import periodicRemoval

if __name__ == "__main__":
    periodicRemoval()
    keepAlive()
    runDiscordBot()