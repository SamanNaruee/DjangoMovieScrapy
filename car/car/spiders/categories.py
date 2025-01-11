import requests
import json

response = requests.get("https://api.digikala.com/v1/categories/")
print(response.status_code)
# data = response.json()

# def extract_category_urls(categories):
#     category_urls = []
#     for category in categories:
#         category_urls.append(category["url"])
#         if "children" in category:
#             category_urls.extend(extract_category_urls(category["children"]))
#     return category_urls

# all_urls = extract_category_urls(data['categories'])
# print(data)
data = json.loads(response.__dict__)
with open('categories.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=True, indent=4))
