from django import template
from apps.story.models import Download

class DownloadCountNode(template.Node):
    def __init__(self, content_object, context_name):
        self.content_object = template.Variable(content_object)
        self.context_name = context_name
    def render(self, context):
        content_object = self.content_object.resolve(context)
        context[self.context_name] = Download.objects.filter(story=content_object).count()
        return ''
    
def do_get_download_count(parser, token):
    error_message = "%r tag must be of format {%% %r for OBJECT as CONTEXT_VARIABLE %%}" % (token.contents.split()[0], token.contents.split()[0])
    try:
        split = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, error_message
    if split[1] != 'for' or split[3] != 'as':
        raise template.TemplateSyntaxError, error_message
    return DownloadCountNode(split[2], split[4])

register = template.Library()
register.tag('get_download_count', do_get_download_count)