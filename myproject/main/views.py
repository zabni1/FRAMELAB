from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .models import Language, LanguageDetail, LanguageDetailCategory, Saved


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
            if query:
                language = LanguageDetail.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:9]
                return render(request, 'partials/search.html', {'language': language})
            else:
                language = context['languages']
                return render(request, 'partials/search.html', {'language': language})
        return render(request, 'main/index.html', context)


class CategoryPageView(ListView):
    template_name = 'main/category.html'
    context_object_name = 'categories'
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
        return LanguageDetail.objects.filter(lang__slug=self.kwargs['show_cat']).select_related('cat')


class UpdateSavedView(View):
    def get(self, request, show_cat):
        if request.headers.get('HX-Request'):
            update_slug = request.GET.get('update_slug')
            delete_slug = request.GET.get('delete_slug')
            if update_slug:
                Saved.objects.create(email=request.user.username,
                                    detail=LanguageDetail.objects.get(slug=update_slug))
                saved = Saved.objects.filter(email=request.user.email).values_list("detail_id", flat=True)
                categories = LanguageDetail.objects.filter(lang__slug=show_cat).select_related('cat')
                context = {'categories': categories, 'saved': saved}
                return render(request, 'partials/category_update.html', context)
            elif delete_slug:
                get = Saved.objects.get(email=request.user.username,
                                             detail=LanguageDetail.objects.get(slug=delete_slug))
                get.delete()
                saved = Saved.objects.filter(email=request.user.email).values_list("detail_id", flat=True)
                categories = LanguageDetail.objects.filter(lang__slug=show_cat).select_related('cat')
                context = {'categories': categories, 'saved': saved}
                return render(request, 'partials/category_delete.html', context)
        return reverse('category_page',  kwargs={'show_cat': show_cat})



class DetailPageView(DetailView):
    template_name = 'detail.html'
    model = LanguageDetail
    slug_url_kwarg = 'show_more'
    context_object_name = 'detail'


class AboutPageView(TemplateView):
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        return context


def test_view(request):
    test = 'test'
    return render(request, 'main/test.html',{'show_cat': test})

def save_test(request, show_cat):
    if request.headers.get('HX-Request'):
        update_slug = request.GET.get('update_slug')
        delete_slug = request.GET.get('delete_slug')
        if update_slug:
            return render(request, 'partials/cat_update.html',{'update_slug': update_slug, 'cat': show_cat})

        elif delete_slug:
            return render(request, 'partials/cat_delete.html', {'delete_slug': delete_slug, 'cat': show_cat})
    return reverse('category', kwargs=show_cat)


def error_view(request, exception):
    return render(request, 'main/error.html', {'exception': exception})
