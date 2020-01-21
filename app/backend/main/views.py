import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse

from musicavis.settings import EXPORTS_DIR, MIMETYPES
from app.models.profile import get_profile_from_user
from app.backend.utils.export import FileDeleteWrapper


def index_view(request):
    if request.user.is_anonymous:
        args = dict(
            export_extensions=['pdf', 'docx', 'xlsx', 'csv', 'txt', 'json', 'xml', 'odt', 'ods'],
            num_love_trees=range(6),
        )
    else:
        args = {'title': 'Home'}

    return render(request, 'main/index.html', args)


def sitemap_view(request):
    args = {'title': 'Sitemap Map'}
    return render(request, 'main/sitemap.html', args)


def pricing_view(request):
    args = {'title': 'Pricing'}
    return render(request, 'main/pricing.html', args)


def features_view(request):
    args = {'title': 'Product Features'}
    return render(request, 'main/features.html', args)


@login_required
def notifications_route(request):
    since = request.GET.get('since', 0.0)
    profile = get_profile_from_user(request.user)
    all_notifications = (profile.notifications
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
    profile = get_profile_from_user(request.user)
    profile.notifications.filter(name=name).delete()

    filepath = f'{EXPORTS_DIR}/{fname}'
    chunksize = 16384
    wrapper = FileDeleteWrapper(filepath=filepath, filelike=open(filepath, 'rb'), blksize=chunksize)

    response = StreamingHttpResponse(wrapper)
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = f"attachment; filename={fname}"
    response['Content-Type'] = MIMETYPES.guess_type(fname)[0]
    return response
