# Simple usage
from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
import os

# path = "C://Users//jerem//OneDrive//Desktop//Coding//Python//SCOPE//"
# os.chdir(path)

nlp = StanfordCoreNLP(path_or_host=r"JavaLibraries", quiet=False)

df = pd.read_csv("urls.csv")

article_text_list = df['text'].to_list()

final_list = []

for text in article_text_list:

    # sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
    # print ('Tokenize:', nlp.word_tokenize(sentence))
    # print ('Part of Speech:', nlp.pos_tag(sentence))
    entity_list = nlp.ner(text)
    # print ('Constituency Parsing:', nlp.parse(sentence))
    # print ('Dependency Parsing:', nlp.dependency_parse(sentence))

    refined_entity_list = []

    for i in range(len(entity_list)):
        if entity_list[i][1] != 'O':
            refined_entity_list.append(entity_list[i])

    final_list.append(refined_entity_list)
    entity_list = []


# print(entity_list[0])
# print(type(entity_list[0]))
# print(entity_list[0][0])
# print(entity_list[0][1])
df['Extracted Entities'] = final_list

df.to_csv("urls_with_entities.csv", index=False)

nlp.close() # Do not forget to close! The backend server will consume a lot memery.
