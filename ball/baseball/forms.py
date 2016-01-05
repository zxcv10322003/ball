from django import forms
from baseball.models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label='分類名稱', help_text='(請輸入分類名稱)')
 
    class Meta:
        model = Category
        fields = ('name', )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='影片標題')
    url = forms.URLField(max_length=128, label='影片網址')
 
    class Meta:
        model = Page
        exclude = ('category', 'views')
        
        
    def clean(self):
        cleanedData = self.cleaned_data
        url = cleanedData.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleanedData['url'] = url
        return cleanedData
        
        
class NameForm(forms.Form):
        name = forms.CharField(max_length=100, label='姓名')
    