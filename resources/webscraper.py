from boilerpy3 import extractors

url = "https://www.cnn.com/2021/09/24/politics/senate-race-rankings-september/index.html"

extractor = extractors.ArticleExtractor()
try:
    doc = extractor.get_doc_from_url(url)
except:
    errors.append(url)
else:
    print(doc.content)
