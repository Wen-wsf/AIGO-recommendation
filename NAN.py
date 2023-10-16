import pandas as pd

'''csv_file_path = "wahooo_data\product_all.csv"  # 請替換為您的 CSV 檔案路徑

# 使用 Pandas 讀取 CSV 檔案
df = pd.read_csv(csv_file_path)

# 檢查是否有空值
null_values = df.isnull().sum()

if null_values.any():
    print("CSV 檔案中存在空值：")
    print(null_values)
else:
    print("CSV 檔案中沒有空值。")
    import pandas as pd
'''
'''# 讀取 CSV 檔案
csv_file_path = 'D:\林宸秧-基於知識圖神經網路之推薦系統\程式\data_processing\product_data\ML\add_to_cart.csv'  # 請替換為您的 CSV 檔案路徑
df = pd.read_csv(csv_file_path)

# 建立 rating 列，並填入隨機的 1 到 5 的數字
df['rating'] = [random.randint(1, 5) for _ in range(len(df))]

# 儲存修改後的 CSV 檔案
output_file_path = 'ML\\add_to_cart.csv'  # 請替換為您想要儲存的修改後的 CSV 檔案路徑
df.to_csv(output_file_path, index=False)

print("CSV 檔案已修改並儲存。")
'''
import pandas as pd

# 讀取評分預測資料表
file_path = r'D:\林宸秧-基於知識圖神經網路之推薦系統\程式\data_processing\product_data\ML\user_rel_item_final_ramdom.csv'  # 請替換為您的資料表路徑
data = pd.read_csv(file_path)

# 根據使用者和物品進行排序，並保留最後一次評分
data_no_duplicates = data.sort_values(by=['UserId', 'MovieId']).drop_duplicates(subset=['UserId', 'MovieId'], keep='last')


# 將處理後的資料保存到新的CSV檔案
output_file_path = r'D:\林宸秧-基於知識圖神經網路之推薦系統\程式\data_processing\product_data\ML\user_rel_item_final_ramdom.csv'  # 請替換為您想要儲存的檔案路徑
data_no_duplicates.to_csv(output_file_path, index=False)



