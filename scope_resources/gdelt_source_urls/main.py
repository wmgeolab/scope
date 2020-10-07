import pandas as pd

def iter_gdelt_sources(file_url):

    # read the mentions csv file
    mentions = pd.read_csv(file_url)
    # store only the language code
    mentions['MentionDocTranslationInfo'] = mentions['MentionDocTranslationInfo'].str[6:9]


    # loop through rows and yield the columns:
    # file_url
    # MentionType
    # MentionSourceName
    # MentionIdentifier
    # MentionDocTranslationInfo (only the language code)
    ment_dict = dict.fromkeys(['file_url', 'MentionType', 'MentionSourceName', 'MentionIdentifier', 'MentionDocTranslationInfo'])

    for column in ['MentionType', 'MentionSourceName', 'MentionIdentifier', 'MentionDocTranslationInfo']:
        data = mentions[column]
        ment_dict[column] = data

    ment_dict['file_url'] = file_url

    yield ment_dict
