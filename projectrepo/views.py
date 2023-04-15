import json

from django.views import generic
from django.core.mail import send_mail, EmailMessage
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

    plagiarism = Plagiarism()
    if data["data"]["attributes"]["resource_type"] == "file" and data["data"]["attributes"]["event_type"] == "file_processed":
        file_id = data["data"]["attributes"]["resource_id"]
        try:
            project = Project.objects.get(file_id=file_id)
        except Project.DoesNotExist:
            return JsonResponse({"Success": False}, status=400)

        plagiarism.start_plagiarism_check(project)
        project.save()
        return JsonResponse({"status": "recieved"})

    if data["data"]["attributes"]["resource_type"] == "similarity_check" and data["data"]["attributes"]["event_type"] == "similarity_check_finished":
        similarity_id = data["data"]["attributes"]["resource_id"]
        try:
            project = Project.objects.get(similarity_check_id=similarity_id)
        except Project.DoesNotExist:
            return JsonResponse({"Success": False}, status=400)

        score, res = plagiarism.fetch_plagiarism_details(project)
        send_mail(subject='final check', message=json.dumps(res), from_email=settings.EMAIL_HOST_USER, recipient_list=["toluhunter19@gmail.com"])

        if score >= 25:
            project.status = "failed"

        else:
            project.status = "verified"

        project.plagiarism_score = score
        project.save()

        plagiarism.re_authenticate()
        plagiarism.export_report(project)
        return JsonResponse({"status": "recieved"})

    if data["data"]["attributes"]["resource_type"] == "similarity_check" and data["data"]["attributes"]["event_type"] == "similarity_check_report_exported":
        link = data["included"][0]["links"]["pdf_report"]
        similarity_id = data["data"]["attributes"]["resource_id"]
        try:
            project = Project.objects.get(similarity_check_id=similarity_id)
        except Project.DoesNotExist:
            return JsonResponse({"Success": False}, status=400)

        response = plagiarism.download_report(project, link)

        mail = EmailMessage(
            "Plagiarism Report",
            "Report can be found as an attachement below",
            settings.EMAIL_HOST_USER,
            [project.scholar.email],
        )
        mail.attach('report.pdf', response.content)
        mail.send(fail_silently=False)

    return JsonResponse({"status": "recieved"})
