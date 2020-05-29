class User():
	"""docstring for User"""
	def __init__(self, user_id, user_name, user_firts_name):
		super().__init__()
		self.user_id = str(user_id)
		self.user_name = str(user_name)
		self.user_firts_name = str(user_firts_name)
		self.karma = 0