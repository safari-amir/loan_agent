from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///loan_management.db")

print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")
