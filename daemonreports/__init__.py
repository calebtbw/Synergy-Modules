from .daemonreports import DaemonReports


def setup(bot):
    bot.add_cog(DaemonReports(bot))
