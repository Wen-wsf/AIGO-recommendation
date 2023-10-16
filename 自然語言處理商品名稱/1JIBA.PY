import jieba
import pandas as pd

data = pd.read_csv('.\Python\del!bewfor_2.csv') 
data.head(100)
product_names = data['product_name']

# 逐個處理每個 product_name
for name in product_names:
    # 使用 jieba 斷詞
    name_str = str(name)  
    segmented_words = jieba.cut(name_str, cut_all=False)
    segmented_result = ' '.join(segmented_words)
    
    print(f"Product Name: {name_str}")
    print(f"Segmented Result: {segmented_result}\n")
