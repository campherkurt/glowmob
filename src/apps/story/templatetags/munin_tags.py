from django import template
from django.conf import settings
import os.path, shutil
register = template.Library()

@register.tag
def munin_graph(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise template.TemplateSyntaxError("%r takes 2 arguments" % bits[0])
    return MuninGraphNode(bits[1],bits[2])

class MuninGraphNode(template.Node):
    
    def __init__(self, variable_name, graph_type):
        self.variable_name = variable_name
        self.graph_type = graph_type
    
    def render(self, context):
        var = context[self.variable_name]
        src = "%s/yoza_%s-%s.png" % (settings.MUNIN_ROOT, var.strip(), self.graph_type.strip())
        dest = "%s/graph_%s_%s.png" % (settings.MEDIA_ROOT, var.strip(), self.graph_type.strip())
        shutil.copyfile(src, dest)
        return "/site_media/media/graph_%s_%s.png" % (var.strip(), self.graph_type.strip())
    
