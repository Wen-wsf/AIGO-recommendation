import pandas as pd

#to_buying = pd.read_csv('.\程式\data_processing\product_data\ML\網頁\\top_buying.csv')
#product_all = pd.read_csv('D:\AI\店商推薦\程式\data_processing\product_data\ML\網頁\product_all.csv')

# 使用merge方法，根據product_id合併兩個DataFrames
#merged = to_buying.merge(product_all[['product_id', 'product_name']], on='product_id', how='left')

# 儲存合併後的DataFrame到新的CSV檔
#merged.to_csv('.\程式\data_processing\product_data\ML\網頁\\top_buying.csv', index=False)
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = int(request.form.get('user').strip())

        return redirect(url_for('recommendations', user=user))
    return render_template('input.html')

@app.route('/recommendations/<user>')
def recommendations(user):
    print(f"Received user: {user}")  # 打印接收到的使用者名稱

    # 讀取CSV檔案
    output_data = pd.read_csv('D:\AI\店商推薦\\output_data.csv')
    product_all = pd.read_csv('D:\AI\店商推薦\程式\data_processing\product_data\ML\網頁\\product_all.csv')
    output_data['User'] = output_data['User'].astype(int)
    print(f"Available users in output_data: {output_data['User'].tolist()}")  # 打印可用的使用者名單

    # 將 user 轉換為浮點數進行匹配
    user_data = output_data[output_data['User'] == float(user)]

    if user_data.empty:
        return "No recommendations found for this user", 404
    # 依據使用者從user_data提取商品ID
    # 使用 dropna() 移除NaN值
    items = user_data.iloc[0, 1:].dropna().values

    # 從product_all提取商品詳細資料
    recommended_products = product_all[product_all['product_id'].isin(items)]

    return render_template('recommendations.html', products=recommended_products)



if __name__ == '__main__':
    app.run(debug=True)

