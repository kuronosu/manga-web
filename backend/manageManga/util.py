""" Clases y Funciones de uso general """
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ImproperlyConfigured
import json

def frontend_permission(view):
    """ Verifica permisos para mostrar o no en el html contenido de staff o author """
    return view.object.author.id == view.request.user.id or view.request.user.is_staff

def filter_obj_model(model, **query_kwargs):
    """ Funcion que filtra objetos de un modelo """
    return model.objects.filter(**query_kwargs)

def chapters_directory_path(instance, filename):
    """
    Funcion que añade retorna una path segun los datos y usuario y archivo
    """
    # file will be uploaded to MEDIA_ROOT/manga/chapter/user_<id>/<filename>
    return 'chapters/{}/{}/{}'.format(
        instance.manga.slug,
        instance.user_chapter_number,
        filename,
        )

def base_data_to_render(request, to_json=False):
    """
    Funcion que retorna todos los datos usados en la peticion al servidor de backend render
    """
    if not (hasattr(request, 'path') and isinstance(request.path, str) and hasattr(request, 'user') and hasattr(request, 'COOKIES') and isinstance(request.COOKIES, dict)):
        raise ImproperlyConfigured("Isn't a valid request object.")
    data = {
        'request_url': request.path,
        'csrftoken': request.COOKIES['csrftoken'],
        'urls': {
            'home': reverse('home'),
            'mangaList': reverse('manageManga:list_of_mangas'),
            'mangaAdd': reverse('manageManga:manga_add'),
            'accountsLogin': reverse('accounts:login') + '?next={}'.format(request.path),
            'accountsSignup': reverse('accounts:singup'),
            'accountsLogout': reverse('accounts:logout') + '?next={}'.format(request.path),
            'accountsPasswordReset': reverse('accounts:password_reset')
        },
        'user': {
            'username': request.user.username,
            'isAthenticated': request.user.is_authenticated
        }
    }
    if to_json:
        return json.dumps(data)
    return data
