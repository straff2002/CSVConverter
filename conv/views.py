from django.shortcuts import render

import make_form
import json
import os
import csv
# Create your views here.



from django.http import HttpResponse
from django.template import loader

from .models import Configurations, ConvertedFiles


def process_error(info,  req):
    return HttpResponse(info)

def get_prev(request):
    config_name = request.POST.getlist("confname")
    if config_name and config_name[0]:
        config_name = config_name[0]
        query = Configurations.objects.filter(config_name=config_name)
        res = query and query[0] or None
        res = res and res.config_text or "No Preview available"
        return res
    else:
        return None
def index(request):
    template = loader.get_template('conv/index.html')
    context = get_page(None)
    conf_res = Configurations.objects.all()
    
    context["conf_files"] = conf_res
    return HttpResponse(template.render(context, request)
                        )
def load(request):
    template = loader.get_template('conv/form.html')
    csv_files = request.FILES.getlist("fileupload")
    if request.POST['config_file'] == "upload":
        try:
            json_file = request.FILES.getlist("config_file_upload")[0]
        except:
            return process_error("Error getting json file", request)
        json_data_s = json_file.read()
        json_data = make_form.parse_config_file(json_data_s)
        if not json_data:
            return process_error("Error parsing the json file", request)
        res = Configurations.objects.filter(config_text=json.dumps(json_data))
        if not res:
            res = Configurations(config_name=json_file.name, config_text=json.dumps(json_data))
            res.save()
    else: #Load the json_data from the database
        json_data = request.POST.getlist('confname')
        json_data = json_data and json_data[0] or None
        conf = Configurations.objects.filter(config_name=json_data)#fixme==>what happens when no matching configuration is found?
        if conf:
            conf = conf[0].config_text
            json_data = make_form.parse_config_file(conf)
        else:
            return process_error("Error retrieving the configuration file from the database.<br/>Ensure you select a pre-existing file.", request)
    table = make_form.main(csv_files, json_data)
    if type(table) != list:

        return process_error(table, request)
    xml_id = request.POST.getlist("xml_id")
    xml_id = xml_id and xml_id[0] or ""
    save_name = request.POST.getlist("save_name")
    save_name = save_name and save_name[0] or None
    context = {'config':json_data,
               'config_s':json.dumps(json_data),
               'table':table,
               'length': len(table[0]),
               'save_name' : save_name,
               'xml_id' : xml_id
                 }

    return HttpResponse(template.render(context, request))
def escape(text):
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;").replace('"', "&qout;").replace("'", "&apos;")

def parse_xml(res_json):
    xml_id = res_json.get("xml_id", "")
    xml_out = '<?xml version="1.0" encoding="UTF-8"?>\n<xmlkfi object_id="%s">\n' %xml_id
    headers = res_json["dest_headers"]
    headers = [escape(h).replace(" ", '') for h in headers]
    for row in res_json["data"]:
        line = '<record>'
        for header, cell, in zip(headers, row):
            line = line + "<" + header + ">" + escape(cell) + "</" + header + ">"
        line = line + "</record>"
        xml_out = xml_out + line + "\n"
    xml_out = xml_out + "</xmlkfi>"
    response = HttpResponse(xml_out, content_type='text/xml')
    save_name = res_json.get("save_name", "Download-data")
    save_name = os.path.splitext(save_name)[0] + ".xml"
    response['Content-Disposition'] = 'attachment; filename="%s"' %save_name
    return response

def parse_csv(res_json):
    response = HttpResponse(content_type='text/csv')
    save_name = res_json.get("save_name", "Download-data")
    save_name = os.path.splitext(save_name)[0] + ".csv"
    response['Content-Disposition'] = 'attachment; filename="%s"' %save_name
    writer = csv.writer(response)
    writer.writerow(res_json.get("dest_headers"))
    for row in res_json.get("data", []):
        writer.writerow(row)
    return response

def convert(request):
    length = int(request.POST.getlist("length")[0])
    cells = request.POST.getlist("cell")
    headers = request.POST.getlist("dest_headers")
    res_json = {'dest_headers':headers, "data":[]}
    for row in range(0, len(cells), length):
        outrow = []
        for x in range(length):
            outrow.append(cells[ x + row] )
        res_json['data'].append(outrow)
    xml_id = request.POST.getlist("xml_id")
    xml_id = xml_id and xml_id[0] or None
    save_name = request.POST.getlist("save_name")
    save_name = save_name and save_name[0] or None
    res_json['xml_id'] = xml_id
    res_json['save_name'] = save_name
    json_s = json.dumps(res_json)
    result = ConvertedFiles.objects.filter(json_text=json_s)
    if not result:
        rec = ConvertedFiles(json_text=json_s, file_name=save_name,  xml_id=xml_id)
        rec.save()
    if request.POST.get("export_as") == "xml":
        return parse_xml(res_json)
    else:
        return parse_csv(res_json)

def get_conf(request):
    confdata = get_prev(request)
    json_data = 1 

    config_name = request.POST.getlist("confname")
    if config_name and config_name[0]:
        config_name = config_name[0]
    else:
        config_name = ""
    query = Configurations.objects.filter(config_name__icontains=config_name)
    res = []
    for r in query:
        res.append((r.id, r.config_name))
    res.sort()
    res = res[:7]
    res = ['<option>%s</option>'%(val[1]) for val in res]
    res = "\n".join(res)
    return HttpResponse(res)

def get_page(request):
    if not request:#create first page view
        last_id = 0
        direction = 'next'
    else:
        last_id = int(request.POST.getlist("last_id")[0])
        direction = request.POST.getlist("direction")[0]
    if direction == 'next':
        start = last_id
        stop = last_id + 15
    else:
        start = max(last_id-30, 0)
        stop = max(last_id -15, 15)
    last_id = stop
    res = ConvertedFiles.objects.order_by('id')[start:stop]
    test = [i.id for i in ConvertedFiles.objects.order_by('id')]
    if not test:#This implies that there are no prior Converted files
        return {'table' : [],
               'last_id' : 15,
               'last' : True,
               'first' : True
               }
    if start not in test:#Ensure start is in test incase it was deleted earlier to avoid index error
        for r in range(len(test) - 1):
            if test[r] < start and test[r+1] > start:
                start = test[r]
        if test and start < test[0]:
            start = test[0]
        if start > test[-1]:
            start = test[-1]
    
    length = len(test)
    length_res = len(res)
    first = (test.index(res[0].id) == 0) #More than one record before the first result
    last = (test[-1] == res[length_res - 1 ].id) #The last record in 'res' is not the last record in the database
    context = {'table' : res,
               'last_id' : last_id,
               'last' : last,
               'first' : first
               }
    if not request:
        return context
    template = loader.get_template('conv/db_data.html')
    return HttpResponse(template.render(context, request))

def get_file(request):
    type = request.GET.get("type")
    id = int(request.GET.get("id"))
    res = ConvertedFiles.objects.get(pk=id)
    data = json.loads(res.json_text)
    sc = {"csv":parse_csv,"xml":parse_xml}
    return sc[type](data)

def getconftable(request):
    if request.POST.get("action") == "use":#It is a POST request
        id = int(request.POST.get("id"))
        res = Configurations.objects.get(pk=id)
        return HttpResponse(str(res.config_name))#Then it is type 'use' in which case we return the name to be set on the 'select' tag 
    #Else, it's a GET request
    id = int(request.GET.get("id"))
    res = Configurations.objects.get(pk=id)
    #If it is type 'view', we return the json text as is
    return  HttpResponse(res.config_text)
