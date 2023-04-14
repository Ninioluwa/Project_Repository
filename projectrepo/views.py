from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from repository.models import Project


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(generic.TemplateView):
    template_name = "index.html"


def webhookview(request):

    if request.method != 'POST':
        return JsonResponse({"Success": False}, status=405)

    project = Project.objects.last()
    project.status = "verified"
    project.save()

    return JsonResponse({"status": "recieved"})
