import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
import pandas as pd
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

data = pd.read_csv('.\程式\自然語言處理商品名稱\data\del!bewfor_14.csv')
data.head(100)
product_names = data['product_name']

# 初始化两个空的列表，用于存
companies = []
products = []

# 定义一个函数来执行NER
def custom_ner(text):
    if not isinstance(text, str):
        text = str(text)  # 轉換成字串
    words = word_tokenize(text)  # 文本分詞
    tagged_words = pos_tag(words)  # 標記磁性

    # 初始化公司名和產品名
    company_name = ""
    product_name = ""

    # 根据詞性来視别公司名和產品名
    for word, pos in tagged_words:
        if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
            # 名詞被視为公司名或產品名的一部分
            if company_name == "":
                company_name = word
            else:
                product_name += " " + word
        elif pos in ['JJ', 'JJR', 'JJS']:
            # 形容詞被視為產品名的一部分
            product_name += " " + word

    return company_name, product_name

for product_name in product_names:
    company, product = custom_ner(product_name)
    companies.append(company)
    products.append(product)
    print("raw product name:", product_name)
    print("brand name:", company)
    print("product:", product)
    print()

result_data = pd.DataFrame({'Company': companies, 'Product': products})

result_data.to_csv('.\程式\自然語言處理商品名稱\data\\NER0.csv', index=False)