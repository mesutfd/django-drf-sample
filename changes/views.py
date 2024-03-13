from django.shortcuts import render, redirect

from changes.forms import ArticleForm


# Create your views here.

def article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')

    else:
        form = ArticleForm()

    return render(request, template_name='article-page.html', context={'form': form})
