import os
import tempfile

from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, StreamingHttpResponse

from musicavis.settings import EXPORTS_DIR, MIMETYPES
from app.models.notification import Notification
from app.backend.utils.export import FileDeleteWrapper


def index_view(request):
    if isinstance(request.user, AnonymousUser):
        args = {
            'export_extensions': ['pdf', 'docx', 'xlsx', 'csv', 'txt', 'json', 'xml', 'odt', 'ods'],
            'num_love_trees': range(6),
        }
    else:
        args = {'title': 'Home'}

    return render(request, 'index.html', args)


def sitemap_view(request):
    args = {'title': 'Sitemap Map'}
    return render(request, 'sitemap.html', args)


def pricing_view(request):
    args = {'title': 'Pricing'}
    return render(request, 'pricing.html', args)


def features_view(request):
    args = {'title': 'Product Features'}
    return render(request, 'features.html', args)


@login_required
def notifications_route(request):
    since = request.GET.get('since', 0.0)
    all_notifications = (request.user.notifications
                         .filter(timestamp__gte=since)
                         .order_by('timestamp'))

    data = {
        "names": [x.name for x in all_notifications],
        "data": [x.payload_json for x in all_notifications],
        "timestamps": [x.timestamp for x in all_notifications]
    }
    return JsonResponse(data, content_type='application/json')


@login_required
def download_file_route(request, fname):
    name = f"export_practice_task_{fname.split('.')[1]}"
    request.user.notifications.filter(name=name).delete()

    filepath = f'{EXPORTS_DIR}/{fname}'
    chunksize = 16384
    wrapper = FileDeleteWrapper(filepath=filepath, filelike=open(filepath, 'rb'), blksize=chunksize)

    response = StreamingHttpResponse(wrapper)
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = f"attachment; filename={fname}"
    response['Content-Type'] = MIMETYPES.guess_type(fname)[0]
    return response
