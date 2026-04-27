from django.db.models import Count
from .models import Comment, Likes, Reply




class DataMixin:
    def get_mixin_context(self, context, email, **kwargs):
        context['likes_com'] = Likes.objects.filter(email=email).values_list('email', flat=True)
        context['comment_user'] = Comment.objects.filter(email=email).values_list('pk', flat=True)
        context.update(kwargs)
        return context

    def get_context_comments(self, pk, email):
        topic_id = pk
        comment = Comment.objects.filter(topic_id=pk).annotate(all_likes=Count('likes'),
                                                                all_replies=Count('replies', distinct=True)).order_by('created_at')
        likes_com = Likes.objects.filter(email=email).values_list('email', flat=True)
        comment_user = Comment.objects.filter(email=email).values_list('pk', flat=True)
        context = {
            'topic_id': topic_id,
            'comment': comment,
            'likes_com': likes_com,
            'comment_user': comment_user
        }
        return context

    def get_context_replies(self, pk, email):
        replies = Reply.objects.filter(comment_id=pk).annotate(all_likes=Count('likes')).select_related('comment')
        likes_rep = Likes.objects.filter(email=email).values_list('email', flat=True)
        reply_user = Reply.objects.filter(email=email).values_list('pk', flat=True)
        context = {
            'pk': pk,
            'replies': replies,
            'likes_rep': likes_rep,
            'reply_user': reply_user
        }
        return context