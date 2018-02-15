""" Funciones de uso general """

def frontend_permission(obj):
    """ Verifica permisos para mostrar o no en el html contenido de staff o author """
    return obj.object.author.id == obj.request.user.id or obj.request.user.is_staff

def filter_obj_model(model, **query_kwargs):
    """ Funcion que filtra objetos de un modelo """
    return model.objects.filter(**query_kwargs)

def user_directory_path(instance, filename):
    """
    Funcion que añade retorna una path segun los datos y usuario y archivo
    """
    # file will be uploaded to MEDIA_ROOT/manga/chapter/user_<id>/<filename>
    return 'manga/user_{0}_{1}/chapter-{3}/{2}'.format(
        instance.author.id,
        instance.author.username,
        filename,
        instance.user_chapter_number
        )

def page_path(instance, filename):
    return 'manga/user_{0}_{1}/chapter-{3}/page/{2}'.format(
        instance.author.id,
        instance.author.username,
        filename,
        instance.chapter.user_chapter_number
        )
