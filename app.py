from flask import Flask, render_template, request
import urllib.request
import json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

product_data = pd.read_csv('D:\CODE\店商推薦\程式\data_processing\product_data\ML\進azure的資料\product_all.csv')
discounted_products = pd.read_csv('D:\CODE\店商推薦\程式\data_processing\product_data\\product_discount.csv')#放折價
hot_sale = pd.read_csv('D:\CODE\店商推薦\程式\data_processing\product_data\ML\網頁\\top_buying.csv')#放熱門
product_name_to_image = {row['product_name']: row['product_image_url'] for _, row in product_data.iterrows()}

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/home.html', methods=['GET', 'POST'])
def home1():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    #以下是新增的
    if request.method == 'POST':
        user = int(request.form.get('user').strip())
        return redirect(url_for('recommendations', user=user))
    return render_template('login.html')
from flask import request

@app.route('/index.html', methods=['GET', 'POST'])
def index():
    random_discounted_products = discounted_products.sample(n=9)
    random_discounted_products_images = [{'item_name': row['product_name'], 'image_url': row['product_image_url']} \
                                         for _, row in random_discounted_products.iterrows()]
    # 取得隨機熱銷商品的數據
    random_hot_sale = hot_sale.sample(n=9)
    random_hot_sale_images = [
        {'item_name': row['product_name'], 'image_url': row['product_image_url']}
        for _, row in random_hot_sale.iterrows()
    ]
    # 若是POST請求，即用戶提交了表單
    if request.method == 'POST':
        user = request.form.get('user')  # 從表單獲取 user
        
        # 確保 user 是數字
        if not user.isdigit():
            return "Invalid user input", 400

        # 讀取CSV檔案
        output_data = pd.read_csv('D:\CODE\店商推薦\\output_data.csv')
        product_all = pd.read_csv('D:\CODE\店商推薦\程式\data_processing\product_data\ML\網頁\\product_all.csv')
        output_data['User'] = output_data['User'].astype(int)

        # 將 user 轉換為整數進行匹配
        user_data = output_data[output_data['User'] == int(user)]

        # 若用戶資料不存在
        if user_data.empty:
            return "No recommendations found for this user", 404

        # 依據使用者從user_data提取商品ID
        items = user_data.iloc[0, 1:].dropna().values

        # 從product_all提取商品詳細資料
        recommended_products = product_all[product_all['product_id'].isin(items)]

        return render_template('index.html', products=recommended_products,discounted_products=random_discounted_products_images, 
        hot_products=random_hot_sale_images)

    # 若是GET請求，即顯示首頁
    return render_template('index.html')

"""@app.route('/index.html', methods=['GET', 'POST'])
def index():
    random_discounted_products = discounted_products.sample(n=10)
    random_discounted_products_images = [{'item_name': row['product_name'], 'image_url': row['product_image_url']} \
                                         for _, row in random_discounted_products.iterrows()]
    # 取得隨機熱銷商品的數據
    random_hot_sale = hot_sale.sample(n=10)
    random_hot_sale_images = [
        {'item_name': row['product_name'], 'image_url': row['product_image_url']}
        for _, row in random_hot_sale.iterrows()
    ]
    print("Discounted Products: ", random_discounted_products_images)
    print("Hot Sale Products: ", random_hot_sale_images)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        #fi = request.form.get('fi')
        product_id = request.form.get('product_id')
        rating = request.form.get('rating')
        data = {
            "Inputs": {
                "input1": [
                    {
                        'user_id': user_id,
                        #'fi': '0',
                        'product_id': product_id,
                        'rating': rating,
                    }
                ],
            },
            "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/7753e5d4d11c4305a7f3d685d3b6bd73/services/ecb232ae6eb848cd88c28a6a744061d1/execute?api-version=2.0&format=swagger'
        api_key = 'igxheyZni19cA4IgO7OMs5nRd6dHJoMhxpeCjieGgQE022SRTWebpFlvYD81+VYrCZoeQzynWRGC+AMCY97oTw==' # Replace this with the API key for the web service
        #url = 'https://ussouthcentral.services.azureml.net/workspaces/183fbe772425405bb663f91d69378b2a/services/222d62d1757a4b658ba2d9946ba0493c/execute?api-version=2.0&format=swagger'
        #api_key = 'SC3Fiep4k9T3EC1dxpjb0vLglzn9iEgYLFcCPq8kMZ5rp0y2E8os1lFd13Pwsehc84xgN1If3Lm/+AMCy47SXA=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            result_json = json.loads(result.decode('utf-8'))
            print(result_json)
            recommended_items = [entry[f'Item {i}'] for entry in result_json['Results']['output1'] for i in range(1, 10)]
            
            # 取得對應的產品圖片 URL
            recommended_items_with_image = [
                {'item_name': item, 'image_url': product_name_to_image.get(item, '')}
                for item in recommended_items
            ]

            return render_template('index.html', recommended_items=recommended_items_with_image,discounted_products =random_discounted_products_images,hot_products=random_hot_sale_images)
        except urllib.error.HTTPError as error:
            return "An error occurred: " + str(error.code)
    return render_template(
        'index.html', 
        recommended_items=None, 
        discounted_products=random_discounted_products_images, 
        hot_products=random_hot_sale_images


        普通客
    )"""
if __name__ == '__main__':
    app.run(debug=True)
    print('Server is running...')
#url = 'https://ussouthcentral.services.azureml.net/workspaces/183fbe772425405bb663f91d69378b2a/services/222d62d1757a4b658ba2d9946ba0493c/execute?api-version=2.0&format=swagger'
        #api_key = 'SC3Fiep4k9T3EC1dxpjb0vLglzn9iEgYLFcCPq8kMZ5rp0y2E8os1lFd13Pwsehc84xgN1If3Lm/+AMCy47SXA=='