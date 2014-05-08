# Create your views here.
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, View
from .models import Blog, BlogPost
from django.conf import settings

def reset_counts(request, label):
    "Resets counts in the session"
    label = label.lower()
    counts = request.session.get(settings.SESSION_KEY, {})
    if label in counts:
        counts[label] = ''
        request.session[settings.SESSION_KEY] = counts

class BlogPostList(ListView):
    template_name = "planet/planet_entries.html"
    paginate_by = 25
    model = BlogPost
    context_object_name = 'blogposts'

    def get_queryset(self):
        query = super(BlogPostList, self).get_queryset()
        return query.select_related("blog").order_by("-creation_date")

    def get_context_data(self, **kwargs):
        get = self.request.GET.get
        self.topic = 'planet'
        context = super(BlogPostList, self).get_context_data(**kwargs)
        context['page_title'] = "Planet"
        context['topic'] = self.topic
        context['limit'] = get('limit', '')
        context['q'] = get('q', '')
        context['sort'] = get('sort', '')
        context['blogs'] = Blog.objects.all().order_by("-list_order")
        reset_counts(self.request, self.topic)
        return context
