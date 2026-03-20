from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Topic, Comment, Reply


class TopicPageView(ListView):
    template_name = 'topic/main.html'
    context_object_name = 'topics'
    allow_empty = False

    def get_queryset(self):
        return Topic.objects.all()

class TopicUpdatePageView(View):
    pass

class TopicDetailView(DetailView):
    template_name = 'topic/detail.html'
    model = Topic
    context_object_name = 'topic'
    slug_url_kwarg = 'show_detail'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['comment'] = Comment.objects.filter(topic=self.object)
        context['reply'] = Reply.objects.filter(topic=self.object)
        return context

class TopicCreateView(CreateView):
    template_name = 'topic/create.html'
    model = Topic
    fields = ['name', 'about', 'email','username','category']
    success_url = reverse_lazy('topic')


class TopicUpdateView(UpdateView):
    template_name = 'topic/update.html'
    model = Topic

    def get_success_url(self):
        return reverse_lazy('topic')

class TopicDeleteView(DeleteView):
    model = Topic
    success_url = reverse_lazy('topic')




