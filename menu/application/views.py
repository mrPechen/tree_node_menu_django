from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from menu.application.models import Menu


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.filter(slug='menu1').first()
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        return response
