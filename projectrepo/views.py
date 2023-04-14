import json

from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from repository.models import Project
from repository.plagrism import Plagiarism


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(generic.TemplateView):
    template_name = "index.html"


@csrf_exempt
def webhookview(request):

    if request.method != 'POST':
        return JsonResponse({"Success": False}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"Success": False}, status=400)

    if data["data"]["attributes"]["resource_type"] == "similarity_check":
        similarity_id = data["data"]["attributes"]["resource_id"]
        project = Project.objects.filter(similarity_check_id=similarity_id)
        plagiarism = Plagiarism()

        score, _ = plagiarism.fetch_plagiarism_details(project)

        if score > 10:
            project.status = "failed"

        else:
            project.status = "verified"

        project.save()

    return JsonResponse({"status": "recieved"})
