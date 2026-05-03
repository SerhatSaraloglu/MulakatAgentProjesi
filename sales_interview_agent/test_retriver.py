from core.retriever import retrieve_context

query = "itiraz yönetimi nasıl yapılır?"

context = retrieve_context(query, role_name="sales_consultant")

print("GETİRİLEN CONTEXT:\n")
print(context)