from django.forms import ModelForm

from changes.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
