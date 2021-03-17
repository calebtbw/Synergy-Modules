from .synergylogs import SynergyLogs


def setup(bot):
    bot.add_cog(SynergyLogs(bot))
