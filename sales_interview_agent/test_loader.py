from core.loader import load_roles, load_knowledge

roles = load_roles("data/roles.json")
print(roles)

text = load_knowledge("data/knowledge/sales_consultant.txt")
print(text[:200])