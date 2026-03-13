from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .models import Language, LanguageDetail, LanguageDetailCategory


class HomePageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            query = request.GET.get('query')
            language = LanguageDetail.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            return render(request, 'partials/search.html', {'query': query, 'languages': language})
        return render(request, 'main/index.html', context)


class CategoryPageView(ListView):
    template_name = 'main/category.html'
    context_object_name = 'categories'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['lang'] = Language.objects.get(slug=self.kwargs['show_cat'])
        return context

    def get_queryset(self):
        return LanguageDetail.objects.filter(lang__slug=self.kwargs['show_cat']).select_related('cat')


class DetailPageView(DetailView):
    template_name = 'detail.html'
    model = LanguageDetail
    slug_url_kwarg = 'show_more'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        context = super(DetailPageView, self).get_context_data(**kwargs)
        context['language'] =  LanguageDetail.objects.filter(slug=self.kwargs['show_more']).select_related('cat')
        return context



class AboutPageView(TemplateView):
    template_name = ''

class ChatView(View):
    def get(self, request):
        return render(request, 'main/chat.html')

    def post(self, request):
        return render(request, 'main/chat.html')

class UpdateChatView(View):
    pass

def test_view(request):
    return render(request, 'main/test.html')



def error_view(request, exception):
    return render(request, 'main/error.html', {'exception': exception})
