from django import template

register = template.Library()



@register.inclusion_tag("profile_item.html")
def show_profile(user):
    return {"user": user}


@register.simple_tag
def clear_search_url(request):
    getvars = request.GET.copy()
    if "search" in getvars:
        del getvars["search"]
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path



@register.tag
def profilepreference(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 2:
        raise template.TemplateSyntaxError("%r takes 1 arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return ProfilePreferenceNode(bits[1], nodelist_true, nodelist_false)

class ProfilePreferenceNode(template.Node):
    
    def __init__(self, attribute, true_nodelist, false_nodelist):
        self.attribute = attribute
        self.true_nodelist = true_nodelist
        self.false_nodelist = false_nodelist
    
    def render(self, context):
        request = context['request']
        user = request.user
        
        if user.is_anonymous():
            return self.true_nodelist.render(context)
        else:
            profile = user.profile_set.latest('pk')
            if getattr(profile, self.attribute):
                return self.true_nodelist.render(context)
            else:
                return self.false_nodelist.render(context)