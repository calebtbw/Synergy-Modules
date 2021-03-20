from .nodestatus import NodeStatus


def setup(bot):
    bot.add_cog(NodeStatus(bot))
