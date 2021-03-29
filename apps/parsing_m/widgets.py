"""
Custom widgets
"""

from django import forms

class SelectMultipleDropdowns(forms.Widget):
    """Widget to display and update a ManyToManyField as one or more html dropdown selects."""
    template_name = 'parsing_m/widgets/selectmultipledropdowns.html'
    none_value = ('', '')

    def __init__(self, attrs=None, extraselects=1):
        """Args:
        - attrs: html attrs to add to select inputs.
        - extraselects: the number of empty select inputs in addition to the ones for existing data (default is 1).
        """
        super().__init__(attrs)
        self.extraselects = extraselects

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        choices = tuple(self.choices) # each call to self.choices hits the db, instead get the choices only once
        #choices = (self.none_value,) + choices # include empty choice

        values = context['widget']['value'] or [] # gets the values
        for _ in range(self.extraselects):
            values.append('') # include 'extra' empty selects

        subwidgets = [] 
        for i,subval in enumerate(values):
            subname = name # by giving the same name to each form select 'name', they get collected as a list of values in the POST data
            subattrs = context['widget']['attrs'].copy()
            subattrs['id'] = 'id_{}_{}'.format(name, i) # set a unique id for each select
            subw = forms.Select(subattrs, choices=choices).get_context(subname, subval, subattrs)['widget']
            subwidgets.append(subw)

        context['widget']['subwidgets'] = subwidgets
        #print(context)
        
        return context

    def format_value(self, value):
        """Gets a list of values from the db to be sent to the form template.
        """
        #print('format value',repr(value))
        return value

    def value_from_datadict(self, data, files, name):
        """Retrieves and cleans the 'name' values from the submitted form's POST 'data' dict to be sent back to the db.
        """
        #print('value from datadict',data,name)
        values = data.getlist(name)
        values = [v for v in values
                  if v != self.none_value[0]] # ignore empty selects
        return values
    

        
