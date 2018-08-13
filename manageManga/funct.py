""" Funciones de uso general """

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
