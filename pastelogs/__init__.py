from .pastelogs import PasteLogs


def setup(bot):
    bot.add_cog(PasteLogs(bot))
