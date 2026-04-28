from .models import Message
from django.db.models import Q
from google import genai


def get_request(pk, message):
    Message.objects.create(user1=pk,
                           user2=0,
                           message=message)
    messages = Message.objects.filter(Q(user1=pk, user2=0) |
                                      Q(user1=0, user2=pk)).order_by('pk')
    end = messages.count()
    start = int(end) - 1

    context = {
        'message': message,
        'messages': messages[start:end],
    }
    return context


def get_reply(pk, message):
    client = genai.Client(api_key='AIzaSyBcdSjYZnCQUCV4aGq-CuAb48iJ8jwLv0k')
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=message
    )
    Message.objects.create(user1=0,
                           user2=pk,
                           message=response.text)
    messages = Message.objects.filter(Q(user1=pk, user2=0) |
                                      Q(user1=0, user2=pk)).order_by('pk')
    end = messages.count()
    start = int(end) - 1
    context = {
        'messages': messages[start:end],
    }
    return context