from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .models import Language, Technology, TechnologyDetail, Saved
from .forms import LanguageForm
from .utils import DataMixin


class HomePageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['languages'] = Language.objects.all()[::-1]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            query = request.GET.get('query')
            if query:
                language = Technology.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:9]
                return render(request, 'partials/search.html', {'language': language})
            else:
                language = context['languages']
                return render(request, 'partials/search.html', {'language': language})
        return render(request, 'main/index.html', context)


class CategoryPageView(ListView):
    template_name = 'main/category.html'
    context_object_name = 'technology'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['lang'] = Language.objects.get(slug=self.kwargs['show_cat'])
        context['show_cat'] = self.kwargs['show_cat']
        if self.request.user.is_authenticated:
            saved = Saved.objects.filter(email=self.request.user.email).values_list("detail_id", flat=True)
            if saved:
                context['saved'] = saved
                return context
        return context
    def get_queryset(self):
        return Technology.objects.filter(lang__slug=self.kwargs['show_cat']).select_related('lang')


class UpdateSavedView(DataMixin, View):
    def get(self, request, show_cat):
        if request.headers.get('HX-Request'):
            update_slug = request.GET.get('update_slug')
            delete_slug = request.GET.get('delete_slug')
            if update_slug:
                Saved.objects.create(email=request.user.email,
                                    detail=Technology.objects.get(slug=update_slug))
                context = self.get_saves_data(request.user.email, show_cat)
                return render(request, 'partials/category_update.html', context)
            elif delete_slug:
                get = Saved.objects.get(email=request.user.email,
                                        detail=Technology.objects.get(slug=delete_slug))
                get.delete()
                context = self.get_saves_data(request.user.email, show_cat)
                return render(request, 'partials/category_update.html', context)
        return redirect('home')


class TranslatePageView(View):
    def get(self, request):
        if request.headers.get('HX-Request'):
            languages = Language.objects.all()
            return render(request, 'partials/translate.html', {'languages': languages})
        return redirect('home')



class DetailPageView(DetailView):
    template_name = 'detail.html'
    model = Technology
    slug_url_kwarg = 'show_more'
    context_object_name = 'technology'

    def get_context_data(self, **kwargs):
        context = super(DetailPageView, self).get_context_data(**kwargs)
        context['detail'] = TechnologyDetail.objects.filter(tech_id=self.object.pk)
        return context

class AboutPageView(TemplateView):
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        return context


def test_view(request):
    form = LanguageForm()
    return render(request, 'main/test.html', {'form': form})

def save_test(request, key):
    if request.headers.get('HX-Request'):
            return render(request, 'partials/cat_delete.html', {'key': key})
    return reverse('home')


def error_view(request, exception):
    return render(request, 'main/error.html', {'exception': exception})
