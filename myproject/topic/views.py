from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .forms import TopicCreateForm
from .models import Topic, Comment, Reply, Likes
from .utils import DataMixin



class TopicPageView(TemplateView):
    template_name = 'topic/main.html'
    extra_context = {'page': 0}


class TopicUpdatePageView(View):
    def get(self, request, page):
        if request.headers.get('HX-Request'):
            topics_qn = Topic.objects.all()
            start = page
            end = page + 5
            topics = topics_qn[start:end]
            if end >= topics_qn.count():
                return render(request, 'partials/topic_update_last.html', {'topics': topics})
            else:
                return render(request, 'partials/topic_update.html', {'topics': topics, 'page': end})
        return redirect('topic')


class TopicDetailView(DetailView, DataMixin):
    template_name = 'topic/detail.html'
    model = Topic
    context_object_name = 'topic'
    slug_url_kwarg = 'show_detail'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['comment'] = Comment.objects.filter(topic=self.object).annotate(likes=Count('likes', distinct=True),
                                                                                replies=Count('replies', distinct=True)).order_by('created_at')
        if self.request.user.is_authenticated:
           return self.get_mixin_context(context, self.request.user.email, comment=context['comment'])
        return context


class TopicCreateView(CreateView):
    template_name = 'topic/create.html'
    form_class = TopicCreateForm
    model = Topic
    success_url = reverse_lazy('topic')


class TopicUpdateView(UpdateView):
    template_name = 'topic/update.html'
    model = Topic
    form_class = TopicCreateForm
    success_url = reverse_lazy('topic')


class TopicDeleteView(DeleteView):
    model = Topic
    success_url = reverse_lazy('topic')


def create_comment(request, pk):
    if request.headers.get('HX-Request'):
        comment = request.GET.get('comment')
        Comment.objects.create(comment=comment,
                               username=request.user.username,
                               email=request.user.email,
                               topic_id=pk)
        data = DataMixin()
        context = data.get_context_comments(pk=pk, email=request.user.email)
        return render(request, 'partials/comment_update.html', context)
    return redirect('topic')


def delete_comment(request, pk):
    if request.headers.get('HX-Request'):
        a = Comment.objects.get(pk = pk).delete()
        data = DataMixin()
        context = data.get_context_comments(pk=a.topic_id, email=request.user.email)
        return render(request, 'partials/comment_update.html', context)
    return redirect('topic')


def get_input_for_reply(request, pk):
    if request.headers.get('HX-Request'):
        return render(request, 'partials/get_reply_on_comment.html', {'pk': pk})
    return redirect('topic')


def get_input_for_reply_on_reply(request, pk, username):
    if request.headers.get('HX-Request'):
        return render(request, 'partials/get_reply_on_reply.html', {'pk': pk, 'username': username})
    return redirect('topic')


def get_replies(request, pk):
    if request.headers.get('HX-Request'):
        data = DataMixin()
        context = data.get_context_replies(pk=pk, email=request.user.email)
        return render(request, 'partials/reply_comment.html', context)
    return redirect('topic')


def create_reply(request, pk):
    if request.headers.get('HX-Request'):
        reply = request.GET.get('reply')
        Reply.objects.create(email=request.user.email,
                             username=request.user.username,
                             reply=reply,
                             comment_id=pk)
        data = DataMixin()
        context = data.get_context_replies(pk=pk, email=request.user.email)
        return render(request, 'partials/reply_comment.html', context)
    return redirect('topic')


def create_reply_on_reply(request, pk, username):
    if request.headers.get('HX-Request'):
        reply = request.GET.get('reply')
        Reply.objects.create(email=request.user.email,
                             username=request.user.username,
                             reply=reply,
                             reply_to = username,
                             comment_id=pk)
        data = DataMixin()
        context = data.get_context_replies(pk=pk, email=request.user.email)
        return render(request, 'partials/reply_comment.html', context)
    return redirect('topic')


def delete_reply(request, pk):
    if request.headers.get('HX-Request'):
        Reply.objects.get(pk=pk).delete()
        data = DataMixin()
        context = data.get_context_replies(pk=pk, email=request.user.email)
        return render(request, 'partials/reply_comment.html', context)
    return redirect('topic')





