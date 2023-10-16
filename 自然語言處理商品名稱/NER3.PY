import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

nltk.download('punkt')
input_df = r"C:\Users\ntub\Desktop\HaWooo_neo4j\Python\\del!bewfor_2.csv"
data = pd.read_csv(input_df)

product_names = data['product_name'].astype(str)
brand_names = data['brand_name'].astype(str)  # 将brand_name列转换为字符串类型

# 初始化两个空的列表，用于存储品牌名和产品名
brands = []
products = []

# 定义一个函数来标记文本中的公司名
def mark_brands(text, brands):
    words = text.split()
    tags = ["O"] * len(words)  # 初始化所有词的标签为"O"（Outside）

    for brand in brands:
        brand_words = brand.split()
        brand_length = len(brand_words)

        for i in range(len(words)):
            if words[i:i+brand_length] == brand_words:
                tags[i] = "B"  # 当找到公司名的开始时，将第一个词标记为"B"（Begin）
                if brand_length > 1:
                    tags[i+1:i+brand_length] = ["I"] * (brand_length - 1)  # 标记公司名的中间词为"I"（Inside）

    return tags

# 对每个产品名称标记公司名
for product_name, brand_name in zip(product_names, brand_names):
    brand_tags = mark_brands(product_name, brand_name.split())
    product_tags = ["O" if tag == "O" else "P" for tag in brand_tags]  # 将公司名的标签标记为"P"（Product），其他标签为"O"（Outside）

    # 将产品名分为品牌名和产品名两部分
    product_words = product_name.split()
    brand_part = " ".join([word if tag != "O" else "" for word, tag in zip(product_words, brand_tags)])
    product_part = " ".join([word if tag == "O" else "" for word, tag in zip(product_words, product_tags)])

    brands.append(brand_part.strip())
    products.append(product_part.strip())

# 创建DataFrame来显示结果
result_data = pd.DataFrame({"Product Name": product_names, "Brand Name": brands, "Product": products})

# 打印结果的前几行
print(result_data.head(10))