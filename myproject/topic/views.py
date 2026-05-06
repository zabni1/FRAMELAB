from django.db.models import Count
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
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
        context['comment'] = Comment.objects.filter(topic=self.object).annotate(all_likes=Count('likes', distinct=True),
                                                                                all_replies=Count('replies', distinct=True)).order_by('created_at')
        if self.request.user.is_authenticated:
           return self.get_mixin_context(context, self.request.user.email, comment=context['comment'])
        return context


class TopicCreateView(View):
    def get(self, request):
        form = TopicCreateForm
        return render(request, 'topic/create.html', {'form': form})

    def post(self, request):
        form = TopicCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            slug = slugify(title)
            Topic.objects.create(title=title,
                                 description=description,
                                 email = request.user.email,
                                 username=request.user.username,
                                 category=category,
                                 slug=slug)

            return redirect('topic')
        return render(request, 'topic/create.html', {'form': form})


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
        return render(request, 'partials/comment_create.html', context)
    return redirect('topic')


def delete_comment(request, pk):
    if request.headers.get('HX-Request'):
        a = Comment.objects.get(pk = pk)
        data = DataMixin()
        context = data.get_context_comments(pk=a.topic_id, email=request.user.email)
        a.delete()
        return render(request, 'partials/comment_delete.html', context)
    return redirect('topic')

def like_comment(request, pk):
    if request.headers.get('HX-Request'):
        comment = Comment.objects.get(pk = pk)
        Likes.objects.create(comment=comment,
                             email=request.user.email)
        likes = Likes.objects.filter(comment=comment).count()
        context = {'likes': likes,
                   'pk': pk}
        return render(request, 'partials/like_comment.html', context    )
    return redirect('topic')

def delete_like_on_comment(request, pk):
    if request.headers.get('HX-Request'):
        comment = Comment.objects.get(pk=pk)
        Likes.objects.get(comment=comment,
                          email=request.user.email).delete()
        likes = Likes.objects.filter(comment=comment).count()
        context = {'likes': likes,
                   'pk': pk}
        return render(request, 'partials/delete_like_on_comment.html', context)
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
        a = Reply.objects.get(pk=pk)
        data = DataMixin()
        context = data.get_context_replies(pk=a.comment_id, email=request.user.email)
        a.delete()
        return render(request, 'partials/reply_comment.html', context)
    return redirect('topic')

def like_reply(request, pk):
    if request.headers.get('HX-Request'):
        reply = Reply.objects.get(pk=pk)
        Likes.objects.create(reply=reply,
                             email=request.user.email)
        likes = Likes.objects.filter(reply=reply).count()
        context = {'likes': likes,
                   'pk': pk}
        return render(request, 'partials/like_reply.html', context)
    return redirect('topic')

def delete_like_on_reply(request, pk):
    if request.headers.get('HX-Request'):
        reply = Reply.objects.get(pk=pk)
        Likes.objects.get(reply=reply,
                          email=request.user.email).delete()
        likes = Likes.objects.filter(reply=reply).count()
        context = {'likes': likes,
                   'pk': pk}
        return render(request, 'partials/delete_like_on_reply.html', context)
    return redirect('topic')





