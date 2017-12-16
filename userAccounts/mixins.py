""" Mixins """
from django.http import JsonResponse

class AjaxableResponseMixin:
    """
    Mixin to add ajax support a form.
    Must be used with an object-based FormView(e.g. CreateView)
    """
    def form_invalid(self, form):
        """form_invalid method"""
        print(self.request.method)
        response = super().form_invalid(form)
        if self.request.is_ajax():
            print('ajax')
            return JsonResponse(form.errors, status=400)
        else:
            return response
    def form_valid(self, form):
        """
        We make to call the parent's form_valid() method because
        it might do some processing (in the case of CreateView, it will
        call form.save() for example )
        """
        print('form_valid')
        response = super().form_valid(form)
        if self.request.is_ajax():
            print('ajax')
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
