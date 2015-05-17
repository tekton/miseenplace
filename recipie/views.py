from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse
import ujson as json
import logging

from recipie.models import Company, MainDoc

logger = logging.getLogger(__name__)


def index(request):
    return render_to_response("index.html", {}, context_instance=RequestContext(request))


def login(request):
    return render_to_response("login.html", {}, context_instance=RequestContext(request))


@csrf_exempt
def api_create_company(request):
    if request.method == "POST":
        company = Company()
        # Company.name = request.body
        try:
            body = json.loads(request.body)
            if "name" in body:
                company.name = body["name"]
                try:
                    company.save()
                    return JsonResponse({"msg": "company created successfuly",
                                         "name": body["name"]})
                except:
                    return JsonResponse({"msg": "Unable to save company"})
            else:
                return JsonResponse({"msg": "Unable to find name to create company"})
        except Exception as e:
            return JsonResponse({"msg": "Unable to process non JSON body", "raw_error": e})
    else:
        return JsonResponse({"msg": "Unable to process non POST requests"})


@csrf_exempt
def api_create_main_doc(request):
    if request.user.id is None:
        return JsonResponse({"msg": "Invalid user session"})
    user = request.user.id
    try:
        body = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"msg": "Unable to process non JSON body", "raw_error": e})
    mainDoc = MainDoc()
    mainDoc.user = user
    try:
        company = Company.objects.get(name=body["name"])
    except Exception as e:
        print(e)
        return JsonResponse({"msg": "Invalid company passed", "raw_error": "Please ask a contact to look at logs"})
    mainDoc.company = company
    try:
        mainDoc.save()
    except Exception as e:
        return JsonResponse({"msg": "Unable to save mainDoc", "raw_error": e})
    return JsonResponse({"msg": "MainDoc successfuly created: {}".format(str(mainDoc.id)),
                         "id": str(mainDoc.id)})
