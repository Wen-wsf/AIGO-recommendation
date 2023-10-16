import jieba
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizerFast, AutoModel
import torch
import matplotlib.pyplot as plt

# 讀取資料
data = pd.read_csv('D:\AI\店商推薦\程式\data_processing\product_data\ML\進azure的資料\product_all.csv')

product_names = data['product_name']

# 初始化 jieba
jieba.setLogLevel(20)

# 初始化 BERT
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModel.from_pretrained('bert-base-chinese')

# 將產品名稱轉換成向量
vectors = []
for name in product_names:
    segmented_words = jieba.cut(name, cut_all=False)
    segmented_result = ' '.join(segmented_words)
    
    tokens = tokenizer.encode(segmented_result, add_special_tokens=True, truncation=True, padding='max_length', max_length=128, return_tensors='pt')
    with torch.no_grad():
        embeddings = model(input_ids=tokens).pooler_output.numpy()
    vectors.append(embeddings.squeeze())

vectors = np.array(vectors)

# 計算相似性矩陣
similarity_matrix = cosine_similarity(vectors)

# 使用KMeans進行聚合
num_clusters = 10000  # 假設要分成10個群集
kmeans = KMeans(n_clusters=num_clusters)
cluster_labels = kmeans.fit_predict(similarity_matrix)

# 創建一個空的群集字典，用於存儲每個群集的產品名稱
cluster_dict = {i: [] for i in range(num_clusters)}

# 將產品名稱添加到對應的群集中
for i, label in enumerate(cluster_labels):
    cluster_dict[label].append(product_names[i])

# 打印每個群集的聚合結果
for label, products in cluster_dict.items():
    print(f"Cluster {label} - {len(products)} products:")
    for product in products:
        print(product)
    print()

# 在每個群集中選擇一個代表性的名稱，作為聚合後的名稱
aggregated_names = []
for label, products in cluster_dict.items():
    representative_name = products[0]  # 這裡可以根據需求選擇不同的名稱
    aggregated_names.append(representative_name)

# 打印聚合後的名稱
for name in aggregated_names:
    print(name)


#aggregated_data = pd.DataFrame(aggregated_names, columns=['aggregated_product_name'])
#aggregated_data.to_csv('aggregated_product_names.csv', index=False)



