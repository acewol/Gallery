from django import forms

from mainapp.models import Product


class ProductAuctionEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('auction_current_cost',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''