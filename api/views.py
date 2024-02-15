from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api.serializer import InputSerializer
from myapp.views import non_responsive_image, responsive_image, cdn_delivered, cdn_not_delivered, css_not_minify_check,\
    google_analytics_check, page_load_time, old_tag_check, get_favicon, url_canonicaction_check,\
    JS_minify_check, alt_check, score, check_ssl, css_minify_check, data, error_check,\
    h1, h2, meta_description,  meta_description_length, robottxt_check, site,\
    title_lenth, title, screenshot, is_seo_friendly, check_social_networks


class SeoViewSet(ViewSet):
    serializer_class = InputSerializer

    def list(self, request):
        return Response({"detail": "Drop your URL in the field to scrap"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], name='meta-data', url_name='meta-data')
    def metaData(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = meta(serializer.data["url"])
            result = {
                "title": data['Title'],
                "title_length": data['Title length'],
                "meta_description": data['Meta Description'],
                "meta_description_length": data['Meta Description Length'],
                "h1": data["H1"],
                "h2":  data["H2"],
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='performance', url_name='performance')
    def performance(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = perf(serializer.data["url"])
            result = {

                "minified_css": data['Minified CSS'],
                "css_not_minified": data['CSS Not Minified'],
                "minified_js": data['Minified JS'],
                "js_not_minified": data['JS Not Minfied'],
                "elements_delivered_by_cdn": data['Elements Delivered by CDN'],
                "elements_not_delivered_by_cdn": data['Elements Not Delivered by CDN'],
                "old_tags": data['Old tags'],
                # "load_time":  data['Load time'],
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='reference', url_name='reference')
    def reference(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = ref(serializer.data["url"])
            result = {
                "sitemaps": data['Sitemaps'],
                "robot_txt": data['Robot.txt'],
                "page_error": data['Page Error'],
                "ssl_certificate": data['SSL Certificate'],
                "responsive_images": data['Responsive images'],
                "non_esponsive_images": data['Non Responsive images'],
                "image_alt_text_absent": data['Image Alt Text Absent'],
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='advance', url_name='advance')
    def advance(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = adv(serializer.data["url"])
            result = {

                "favicon": data['Favicon'],
                "is_seo_friendly": data['is_seo_friendly'],
                "canonical_url": data['Canonical URL'],
                "google_analytics_test": data['Google analytics Test'],
                "social_media_test": data['Social Media Test'],

            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='score', url_name='score')
    def score(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = scre(serializer.data["url"])
            result = {

                "score": data['Score'],
                # "Image": data['Image'],
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='screenshot', url_name='screenshot')
    def screenshot(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = screen(serializer.data["url"])
            result = {
                "image_path": data['Image URL'],
            }
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def perf(url):
    soup = data(url)
    context = {

        'Minified CSS': css_minify_check(soup),
        'CSS Not Minified': css_not_minify_check(soup),
        'Minified JS': JS_minify_check(soup),
        'JS Not Minfied': JS_minify_check(soup),
        'Old tags': old_tag_check(soup),
        # 'Load time':  page_load_time(url),
        'Elements Delivered by CDN':  cdn_delivered(soup),
        'Elements Not Delivered by CDN':  cdn_not_delivered(soup),

    }
    return context


def meta(url):
    soup = data(url)
    context = {
        "Title": title(soup),
        "Title length": title_lenth(soup),
        "Meta Description": meta_description(soup),
        "Meta Description Length": meta_description_length(soup),
        'H1': h1(soup),
        'H2': h2(soup),

    }
    return context


def ref(url):
    soup = data(url)
    context = {

        'H2': h2(soup),
        'Sitemaps': site(url),
        'Robot.txt': robottxt_check(url),
        'Page Error': error_check(url),
        'SSL Certificate': check_ssl(url),
        'Image Alt Text Absent': alt_check(soup),
        'Responsive images': responsive_image(soup),
        'Non Responsive images': non_responsive_image(soup),


    }
    return context


def adv(url):
    soup = data(url)
    context = {

        'Canonical URL': url_canonicaction_check(url),
        'is_seo_friendly': is_seo_friendly(url),
        'Favicon':  get_favicon(soup, url),
        'Google analytics Test':  google_analytics_check(soup),
        'Social Media Test':  check_social_networks(url),
    }
    return context


def scre(url):
    soup = data(url)
    context = {
        "Score": score(soup, url),
    }
    return context

def screen(url):
    context = {
        'Image URL': screenshot(url)
    }
    return context

