from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse
import ujson as json
import logging

from recipie.models import Company, MainDoc, DefaultDoc, get_defaults, default_document

logger = logging.getLogger(__name__)


def index(request):
    default_docs = DefaultDoc.objects.filter(user=request.user.id)
    for doc in default_docs:
        print(doc.id)
    return render_to_response("index.html", {"default_docs": default_docs,
                                             "active": "home"}, context_instance=RequestContext(request))


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


def form_default_doc_view(request):
    defaults = get_defaults(DefaultDoc)
    return render_to_response('default_doc.html',
                              {"defaults": defaults,
                               "active": "setup"},
                              context_instance=RequestContext(request))


def process_default_doc(request):
    defaults = get_defaults(DefaultDoc)
    if request.method == "POST":
        # lets check to see if it's json or a form encode
        default_doc = DefaultDoc()
        sort_dict = None
        if "oauth" in request.POST:
            print("post soft_dict")
            sort_dict = request.POST
            print(request.POST)
        else:
            try:
                body = json.loads(request.body)
                print("ajax sort_dict")
                if "oauth" in body:
                    sort_dict = body
            except Exception as e:
                print("You done messed up")
                print(e)
                return JsonResponse({"msg": "You done messed up"})

        for x in sort_dict:
            print("Key in sort_dict", x)
            if hasattr(default_doc, x):
                if x == "user":
                    default_doc.user = request.user.id
                elif sort_dict[x] is not None and sort_dict[x] is not u'':
                    print("Setting", x, "to", sort_dict[x])
                    default_doc[x] = sort_dict[x]
                else:
                    setattr(default_doc, x, defaults[x])
            else:
                pass
        try:
            default_doc.save()
            return JsonResponse({"msg": "Able to save default doc",
                                 "id": str(default_doc.id)})
        except Exception as e:
            print("Unable to save default doc")
            print(e)
            return JsonResponse({"msg": "Unable to save default doc"})
    else:
        return JsonResponse({"msg": "Unable to process non POST requests"})


def morph_default_doc(request, obj_id):
    print(obj_id)
    try:
        default_doc = DefaultDoc.objects.get(id=obj_id)
    except Exception as e:
        print(e)
        return JsonResponse({"msg": "Unable to find requested default document"})
    out_doc = default_document
    for field in DefaultDoc._fields_ordered:
        # the following should be able to be int he same line but it was causing issues _sometimes_
        old = "[[{}]]".format(field)
        new = str(getattr(default_doc, field))
        out_doc = out_doc.replace(old, new)
    return HttpResponse(out_doc, content_type='text/plain')
