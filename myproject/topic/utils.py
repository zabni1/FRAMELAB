from django.db.models import Count
from .models import Comment, Likes, Reply




class DataMixin:
    def get_mixin_context(self, context, email, **kwargs):
        context['likes_com'] = Likes.objects.filter(email=email).values_list('comment_id', flat=True)
        context['comment_user'] = Comment.objects.filter(email=email).values_list('pk', flat=True)
        context.update(kwargs)
        return context

    def get_context_comments(self, pk, email):
        comments = Comment.objects.filter(topic_id=pk).annotate(likes=Count('likes'))
        likes_com = Likes.objects.filter(email=email).values_list('comment_id', flat=True)
        comment_user = Comment.objects.filter(email=email).values_list('pk', flat=True)
        context = {
            'comments': comments,
            'likes_com': likes_com,
            'comment_user': comment_user
        }
        return context

    def get_context_replies(self, pk, email):
        replies = Reply.objects.filter(comment_id=pk).annotate(likes=Count('likes')).select_related('comment')
        likes_rep = Likes.objects.filter(email).values_list('reply_id', flat=True)
        reply_user = Reply.objects.filter(email).values_list('pk', flat=True)
        context = {
            'replies': replies,
            'likes_rep': likes_rep,
            'reply_user': reply_user
        }
        return context