import jieba
import pandas as pd
import torch
from transformers import BertTokenizerFast, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# 檢查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 載入中文的 BERT 模型
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModel.from_pretrained('ckiplab/bert-base-chinese').to(device)

data = pd.read_csv('C:\\Users\\ntub\\Desktop\\HaWooo_neo4j\\Python\\product_all.csv')

data = data.head(10000)
product_names = data['product_name']
# 定義關鍵字和閾值
keywords_to_remove = ["限時", "數量有限", "限量", "直播限定", '限时', '限定', "节限定"]
similarity_threshold = 0.5
# 儲存向量的列表
vectors = []

# 定義批次大小
batch_size = 32

# 逐批次處理產品名稱
for i in range(0, len(product_names), batch_size):
    batch_names = product_names[i:i + batch_size]
    batch_vectors = []

    for name in batch_names:
        # 使用 jieba 斷詞
        segmented_words = jieba.cut(name, cut_all=False)
        segmented_result = ' '.join(segmented_words)
        # 計算分詞後的向量
        tokens = tokenizer.tokenize(segmented_result)
        ids = tokenizer.convert_tokens_to_ids(tokens)
        ids_tensor = torch.tensor([ids]).to(device)
        # 使用 BERT tokenizer 將句子轉換為向量
        inputs = tokenizer(segmented_result, return_tensors='pt').to(device)
        with torch.no_grad():
            vector = model(ids_tensor).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        # 找到相似的詞並刪除
        similar_words = []
        for keyword in keywords_to_remove:
            keyword_tokens = tokenizer.tokenize(keyword)
            keyword_ids = tokenizer.convert_tokens_to_ids(keyword_tokens)
            keyword_ids_tensor = torch.tensor([keyword_ids]).to(device)
            with torch.no_grad():
                keyword_vector = model(keyword_ids_tensor).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

            similarity = cosine_similarity([vector], [keyword_vector])
            if similarity >= similarity_threshold:
                similar_words.append(keyword)

        # 刪除相似詞
        filtered_words = [word for word in segmented_result.split() if word not in similar_words]
        filtered_result = ' '.join(filtered_words)

        vectors.append(vector)
        batch_vectors.append(vector)

    print(f"Processed batch {i // batch_size + 1}")
    print(f"Product Name: {name}")
    print(f"segmented_result: {segmented_result}")
    print(f"Vector: {vector}\n")

# 轉換向量列表為DataFrame
vectors_df = pd.DataFrame(vectors)

# 將原始資料與向量合併
data_with_vectors = pd.concat([data, vectors_df], axis=1)

data_with_vectors.to_csv('C:\\Users\\ntub\\Desktop\\HaWooo_neo4j\\Python\\product_all_del.csv', index=False)
