
from django.forms import ModelForm

from domain.models import SourceCode
from .models import Source


class SourceForm(ModelForm):
    class Meta:
        model = Source
        exclude = []

    def clean_source_text(self):
        # retrieve the text for the source
        data = self.cleaned_data['source_text']
        code = self.data['source_code']
        if data == "": #with this, it should work for either source_add or source_import (for any empty rows)
            if code == "SCOPE_S_1": #currently, this method is limited to articles (media reports)
                url = self.data['source_url']
                import requests
                exist = requests.head(url).status_code
                if (exist < 400 or exist > 499):
                    from boilerpy3 import extractors
                    import re
                    extractor = extractors.ArticleExtractor()
                    doc = extractor.get_doc_from_url(url)
                    #may reassess which spacing and punctuation to include in the future
                    content = doc.content.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\f', ' ').replace('\v', ' ')
                    content = re.sub(r'\s+', ' ', content)
                    data += content
                    #content_nopunc = re.sub('[^a-zA-Z]', ' ', content)
                    #content_nopunc = re.sub(r'\s+', ' ', content_nopunc)

        return data

    def clean_source_html(self):
        # retrieve the html for the source
        data = self.cleaned_data['source_html']
        code = self.data['source_code']
        if data == "":
            if code == "SCOPE_S_1":
                url = self.data['source_url']
                import requests
                exist = requests.head(url).status_code
                if (exist < 400 or exist > 499):
                    r = requests.get(url)
                    data += r.text
        return data