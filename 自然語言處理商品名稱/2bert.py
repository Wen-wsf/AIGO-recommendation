import torch
import numpy as np
from transformers import BertTokenizerFast, AutoModel

# 檢查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModel.from_pretrained('ckiplab/bert-base-chinese').to(device)

words_to_embed = ["限時", "數量有限", "限量", "直播限定", '限时', '限定', "节限定"]

# 初始化嵌入向量的列表
embeddings = []

# 逐個處理每個詞彙並生成嵌入向量
for word in words_to_embed:
    # 將詞彙轉換為向量
    tokens = tokenizer.tokenize(word)
    ids = tokenizer.convert_tokens_to_ids(tokens)
    ids_tensor = torch.tensor([ids]).to(device)
    # 模型生成詞彙的向量表示
    with torch.no_grad():
        vector = model(ids_tensor).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    
    embeddings.append(vector)

embeddings = torch.tensor(embeddings)

print(embeddings)
