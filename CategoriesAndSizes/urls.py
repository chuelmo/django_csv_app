from django.urls import re_path, path
from . import views

# namespace
app_name = "CategoriesAndSizes"

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('categories/', views.listCategories),
    path('categories/add/', views.createCategory),
    path('categories/del/<id>', views.deleteCategory),
    path('categories/edit/<id>', views.editCategory),
    path('categories/update/', views.updateCategory),
    path('talles/<idCategory>', views.listSizes),
    path('talles/add/', views.createSize),
    path('talles/edit/<id>/<idCat>', views.editSize),
    path('talles/update/', views.updateSize),
    path('talles/del/<id>/<idCat>', views.deleteSize),
    re_path(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    re_path(r'^delete/$', views.model_delete, name='model_delete'),
    re_path(r'^download/(?P<id>.*)/$', views.file_response_download, name='file_download'),
    path('pdf/', views.export_pdf_categories, name="export-pdf_categories"),
    path('export_pdf_sizes/<id>', views.export_pdf_sizes, name='export_pdf_sizes'),
]