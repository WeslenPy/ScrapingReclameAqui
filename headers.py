from fake_useragent import UserAgent

#User Agent Aleatório
user_agent = UserAgent()

#Header API ID
header = {
'Accept': 'application/json, text/plain, */*',
'User-Agent': str(user_agent.chrome)}
