from src.github_api import get_user_profile, get_user_repos, get_user_events
from src.analyzer import analyze_profile

p = get_user_profile('Namra-Haseeb')
r = get_user_repos('Namra-Haseeb')
e = get_user_events('Namra-Haseeb')
result = analyze_profile(p, r, e)
print(result)
