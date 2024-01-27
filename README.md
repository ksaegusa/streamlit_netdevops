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