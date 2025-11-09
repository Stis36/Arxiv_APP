import pprint
import arxiv
import pandas as pd

# 新しい arxiv API を使用
client = arxiv.Client()
search = arxiv.Search(
    query='au:"Grisha Perelman"',
    max_results=10,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# 検索結果をリストに変換
l = list(client.results(search))

print(type(l))
# <class 'list'>

print(len(l))
# 3

print(type(l[0]))
# <class 'arxiv.Result'>