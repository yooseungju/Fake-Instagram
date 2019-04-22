
from django import template
register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content+' '
    hashtags = post.hashtags.all()
    
    def atag(s):
        return f"<a href = '/posts/hashtag/{s.id}'>{s.content}</a>"+" "
    for hashtag in hashtags:
        content = content.replace(hashtag.content+' ', atag(hashtag))
    return content
    