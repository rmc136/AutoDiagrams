from django.urls import path
from .views import UploadYAMLView, GenerateDiagramView, RetrieveDiagramView, ListDiagramsView, DeleteDiagramView
from api.views import upload_success_view, upload_yaml_view, regenerate_diagram_view, usage_toturial
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', upload_yaml_view, name='upload_yaml'),
    path('upload/success/<int:diagram_id>/', upload_success_view, name='upload_success'),
    path('upload/', UploadYAMLView.as_view(), name='upload_yaml'),
    path('generate/', GenerateDiagramView.as_view(), name='generate_diagram'),
    path('diagram/<int:diagram_id>/', RetrieveDiagramView.as_view(), name='retrieve_diagram'),
    path('diagrams/', ListDiagramsView.as_view(), name='list_diagrams'),
    path('diagram/<int:diagram_id>/delete/', DeleteDiagramView.as_view(), name='delete_diagram'),
    path('regenerate/<int:diagram_id>/', regenerate_diagram_view, name='regenerate_diagram'),
    path('usage/', usage_toturial, name='usage_tutorial'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)