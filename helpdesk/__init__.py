from .helpdesk import HelpDesk


def setup(bot):
	bot.add_cog(HelpDesk(bot))
