from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from weasyprint import HTML
import os
from .forms import FileUploadModelForm
from .models import SizeCategory, Size, File
from .procesar_csv import procesarCSV

def home(request):
    return render(request, "home.html")

@login_required(login_url="/accounts/login/")
def listCategories(request):
    allCategories = SizeCategory.objects.all()
    return render(request, 'crudCategories.html', {'categories': allCategories})

@login_required(login_url="/accounts/login/")
def listSizes(request, idCategory):
    categoria = SizeCategory.objects.get(id=idCategory)
    sizes = SizeCategory.objects.get(id=idCategory).size_set.all()
    return render(request, 'crudTalles.html', {'category': categoria, 'sizes': sizes})

@login_required(login_url="/accounts/login/")
def createCategory(request):
    nombre = request.POST['txtDescription']
    categoria = SizeCategory.objects.create(description=nombre)
    return redirect('/files/categories/')

@login_required(login_url="/accounts/login/")
def createSize(request):
    idCategoria = request.POST['txtIdCat']
    nombre = request.POST['txtNombreSize']
    categoria = SizeCategory.objects.get(id=idCategoria)
    size = Size(name=nombre)
    size.save()
    size.categories.add(categoria)
    return redirect('/files/talles/' + idCategoria)

@login_required(login_url="/accounts/login/")
def editCategory(request, id):
    categoria = SizeCategory.objects.get(id=id)
    return render(request, "editCategory.html", {"category": categoria})

@login_required(login_url="/accounts/login/")
def editSize(request, id, idCat):
    talle = Size.objects.get(id=id)
    return render(request, "editSize.html", {"size": talle, "category": idCat})

@login_required(login_url="/accounts/login/")
def deleteCategory(request, id):
    categoria = SizeCategory.objects.get(id=id)
    categoria.delete()
    return redirect('/files/categories/')

@login_required(login_url="/accounts/login/")
def deleteSize(request, id, idCat):
    size = Size.objects.get(id=id)
    size.delete()
    return redirect('/files/talles/' + idCat)

@login_required(login_url="/accounts/login/")
def updateCategory(request):
    id = request.POST['txtId']
    nombre = request.POST['txtDescription']
    categoria = SizeCategory.objects.get(id=id)
    categoria.description = nombre
    categoria.save()
    return redirect('/files/categories/')

@login_required(login_url="/accounts/login/")
def updateSize(request):
    id = request.POST['txtId']
    nombre = request.POST['txtNombre']
    idCategoria = request.POST['txtCategoria']
    talle = Size.objects.get(id=id)
    talle.name = nombre
    talle.save()
    return redirect('/files/talles/' + idCategoria)

@login_required(login_url="/accounts/login/")
def file_list(request):
    files = File.objects.all().order_by("-id")
    deletedFiles = False
    for f in files:
        if not f.file.storage.exists(f.file.name):
            f.delete()
            deletedFiles = True
    if deletedFiles:
        files = File.objects.all().order_by("-id")
    return render(request, 'file_list.html', {'files': files})

@login_required(login_url="/accounts/login/")
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/files/")
    else:
        form = FileUploadModelForm()
    return render(request, 'upload_form.html', {'form': form, 'heading': 'Subir csv para agregarle los Sizes'})

@login_required(login_url="/accounts/login/")
def file_response_download(request, id):
    file = File.objects.get(pk=id)
    file_path = file.file.url[1:]
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    ext = os.path.basename(file_path).split('.')[-1].lower()
    if ext in ['csv']:
        todoOK = procesarCSV(os.path.join(media_root, 'files', os.path.basename(file.file.url)))
        if todoOK[0] == 'OK':
            response = FileResponse(open(file_path, 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        else:
            return render(request, 'errors_list.html', {'errors': todoOK})
    else:
        raise Http404

@login_required(login_url="/accounts/login/")
def model_delete(request):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    records = File.objects.all()
    for f in records:
        fileName = os.path.join(media_root, 'files', os.path.basename(f.file.url))
        if os.path.isfile(fileName):
            os.remove(fileName)
    records.delete()
    return render(request, 'file_list.html', {'files': records})

@login_required(login_url="/accounts/login/")
def export_pdf_categories(request):
    categories = SizeCategory.objects.all()
    context = {}
    for c in categories:
        context[c.id] = c.description
    html = render_to_string("report-pdf.html", {'context': context})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    HTML(string=html).write_pdf(response)
    return response

@login_required(login_url="/accounts/login/")
def export_pdf_sizes(request, id):
    categoria = SizeCategory.objects.get(id=id)
    sizes = SizeCategory.objects.get(id=id).size_set.all()
    talles = {}
    for size in sizes:
        talles[size.id] = size.name
    html = render_to_string("report-talles.html", {'categoria': categoria.description, 'sizes': talles})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    HTML(string=html).write_pdf(response)
    return response
