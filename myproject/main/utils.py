from .models import Technology, Saved


class DataMixin:
    def get_saves_data(self, email, show_cat):
        saved = Saved.objects.filter(email=email).values_list("detail_id", flat=True)
        categories = Technology.objects.filter(lang__slug=show_cat).select_related('cat')
        context = {'categories': categories, 'saved': saved}
        return context