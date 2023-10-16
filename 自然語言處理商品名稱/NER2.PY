import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

nltk.download('punkt')

product_names = [
    "真女人 蘆薈修護凝膠",
    "玉如阿姨 女人V機密內衣（藍色）",
    "Sunart 玻璃杯│小丑",
    "YoDa 6in1多功能座椅式抱嬰揹帶-異國綠",
    "YoDa 和風透氣四層紗扣扣兜-夢之水手",
    "FM Shoes 韓流時尚NEU TRAL棉質慢跑鞋 ( 訂製款 )"
]

brand_names = ["真女人", "玉如阿姨", "Sunart", "YoDa", "FM Shoes"]

brands = []
products = []

# 定义一个函数来标记文本中的公司名
def mark_brands(text, brands):
    words = word_tokenize(text)
    tags = ["O"] * len(words)  # 初始化所有词的标签为"O"（Outside）

    for brand in brands:
        brand_words = word_tokenize(brand)
        brand_length = len(brand_words)

        for i in range(len(words)):
            if words[i:i+brand_length] == brand_words:
                tags[i] = "B"  # 当找到公司名的开始时，将第一个词标记为"B"（Begin）
                if brand_length > 1:
                    tags[i+1:i+brand_length] = ["I"] * (brand_length - 1)  # 标记公司名的中间词为"I"（Inside）

    return tags

# 对每个产品名称标记公司名
for product_name in product_names:
    brand_tags = mark_brands(product_name, brand_names)
    product_tags = ["O" if tag == "O" else "P" for tag in brand_tags]  # 将公司名的标签标记为"P"（Product），其他标签为"O"（Outside）

    # 将产品名分为品牌名和产品名两部分
    product_words = word_tokenize(product_name)
    brand_part = " ".join([word if tag != "O" else "" for word, tag in zip(product_words, brand_tags)])
    product_part = " ".join([word if tag == "O" else "" for word, tag in zip(product_words, product_tags)])

    brands.append(brand_part.strip())
    products.append(product_part.strip())

# 创建DataFrame来显示结果
result_data = pd.DataFrame({"Product Name": product_names, "Brand Name": brands, "Product": products})

# 打印结果
print(result_data)
