from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .forms import QueryForm
from .models import Language, LanguageDetail, LanguageDetailCategory


class HomePageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        context['form'] = QueryForm()
        query = self.request.GET.get('q')
        if query:
            context['languages'] = LanguageDetail.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return context


class CategoryPageView(TemplateView):
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['page'] = 1
        return context


class UpdateCategoryPageView(View):
    def get(self, request):
        if self.kwargs['page'] == 1:
            context = {
            'detail': LanguageDetail.objects.filter(lang__slug=self.kwargs['show_cat'],cat_id=self.kwargs['page']),
            'category': LanguageDetailCategory.objects.get(id=self.kwargs['page']),
            'page': self.kwargs['page'] + 1
            }
            return render(request, '', context)
        else:
            context = {
            'detail': LanguageDetail.objects.filter(lang__slug=self.kwargs['show_cat'],cat_id=self.kwargs['page']),
            'category': LanguageDetailCategory.objects.get(id=self.kwargs['page'])
            }
            return render(request, '', context)



class DetailPageView(DetailView):
    template_name = ''
    model = LanguageDetail
    slug_url_kwarg = 'show_more'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        context = super(DetailPageView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return LanguageDetail.objects.filter(slug=self.kwargs['show_more']).select_related('cat')


class AboutPageView(TemplateView):
    template_name = ''

class ChatView(View):
    def get(self, request):
        return render(request, 'main/chat.html')

    def post(self, request):
        return render(request, 'main/chat.html')

class UpdateChatView(View):
    pass

def error_view(request, exception):
    return render(request, 'main/error.html', {'exception': exception})
