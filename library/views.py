import cairosvg
import logging
import mimetypes
import os
import tempfile

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import Image

DEFAULT_COLOR = "#CB4698"


logger = logging.getLogger(__name__)


def index(request):
    images = Image.objects.order_by("created")
    context = {"images": images}

    return render(request, "library/index.html", context)


def detail(request, image_id):
    image = Image.objects.get(id=image_id)
    context = {"image": image}
    return render(request, "library/detail.html", context)


def download(request, image_id, color):
    image = Image.objects.get(id=image_id)

    SVG_DIRS = getattr(settings, "SVG_DIRS", [])

    if type(SVG_DIRS) != list:
        raise ImproperlyConfigured("SVG_DIRS settings must be a list")

    path = None

    if SVG_DIRS:
        for directory in SVG_DIRS:
            svg_path = os.path.join(
                directory, "{filename}.svg".format(filename=image.filename())
            )
            if os.path.isfile(svg_path):
                path = svg_path
    else:
        path = finders.find(
            os.path.join("svg", "{filename.svg}".format(filename=image.filename())),
            all=True,
        )

    if not path:
        message = "SVG '{filename}.svg' not found.".format(filename=image.filename())

        # Raise exception if DEBUG is True, else just log a warning.
        if settings.DEBUG:
            raise FileNotFoundError(message)
        else:
            logger.warning(message)
            return ""

    # Sometimes path can be a list/tuple if there's more than one file found
    if isinstance(path, (list, tuple)):
        path = path[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(path) as svg_file:
            output_path = os.path.join(tmpdir, f"{image.filename()}.png")
            svg = mark_safe(svg_file.read())
            svg = svg.replace(DEFAULT_COLOR, f"#{color}")
            cairosvg.svg2png(bytestring=svg, write_to=output_path)

        fl = open(output_path, "rb")
        mime_type, _ = mimetypes.guess_type(output_path)
        print("DBG!")
        print(output_path)
        print(mime_type)
        response = HttpResponse(fl, content_type=mime_type)
        response["Content-Disposition"] = (
            "attachment; filename=%s" % f"{image.filename()}.png"
        )

        return response
