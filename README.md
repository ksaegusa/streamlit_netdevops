# streamlit_netdevops

## セットアップ
```
pip install -r requirements.txt
```

## サーバー起動
```
streamlit run home.py
```

ポート指定で起動する場合  
```
streamlit run home.py --server.port 80
```

## 機能
1. parser  
テキストエリアに書き込んだテキスト、もしくはアップロードしたテキストをパース。テンプレートはfiles/templatesに格納しているもの、もしくはアップロードが可能。  
パース結果をjmespathで絞り込むクエリの確認がでます。
2. regex  
テキストエリアに書き込んだテキスト、もしくはアップロードしたテキストの行にマッチする正規表現の確認ができます。


## 利用例
1. parser
   テキストとパーサーを選択すると、パース結果が表示されます
   <img width="550" alt="image" src="https://github.com/ksaegusa/streamlit_netdevops/assets/33768444/813f797d-856c-4eb8-9a98-f79e51718cd0">  
   クエリ文を入力し、\[クエリ実行\]をクリックします。クエリ結果が表示されます。
   <img width="586" alt="image" src="https://github.com/ksaegusa/streamlit_netdevops/assets/33768444/9c3b5ea7-70ad-4233-bb3e-dde3b2e69ec0">  
   jmespathのfunctionも利用可能です。
   <img width="582" alt="image" src="https://github.com/ksaegusa/streamlit_netdevops/assets/33768444/61eb8a89-1318-4eb9-8968-6320fa78ff44">  

2. regex
   テキストに対して正規表現のマッチした行を表示させます。
   <img width="609" alt="image" src="https://github.com/ksaegusa/streamlit_netdevops/assets/33768444/504abf06-6d97-440d-96e0-c0f5ec0d9fbd">  
   正規表現を入力し\[抽出\]をクリックします。マッチした行数と文が表示されます。
   <img width="572" alt="image" src="https://github.com/ksaegusa/streamlit_netdevops/assets/33768444/08717c50-707c-4679-ad30-9904257c0130">  



   
