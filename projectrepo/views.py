import json

from django.views import generic
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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

    if data["data"]["attributes"]["resource_type"] == "similarity_check" and data["data"]["attributes"]["event_type"] == "similarity_check_finished":
        similarity_id = data["data"]["attributes"]["resource_id"]
        try:
            project = Project.objects.get(similarity_check_id=similarity_id)
        except Project.DoesNotExist:
            return JsonResponse({"Success": False}, status=400)

        plagiarism = Plagiarism()

        score, _ = plagiarism.fetch_plagiarism_details(project)

        if score >= 25:
            project.status = "failed"

        else:
            project.status = "verified"

        project.plagiarism_score = score
        project.save()

        plagiarism.re_authenticate()
        plagiarism.export_report(project)
        project.save()
        return JsonResponse({"status": "recieved"})

    if data["data"]["attributes"]["resource_type"] == "similarity_check" and data["data"]["attributes"]["event_type"] == "similarity_check_report_exported":
        job_id = data["data"]["attributes"]["resource_id"]

        try:
            project = Project.objects.get(job_id=job_id)
        except Project.DoesNotExist:
            return JsonResponse({"Success": False}, status=400)
        send_mail(subject='Plagiarism Report', message="Report Downloaded",
                  from_email=settings.EMAIL_HOST_USER, recipient_list=[project.scholar.email])

        plagiarism.download_report(project)

    return JsonResponse({"status": "recieved"})
