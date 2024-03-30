from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class ShopUserRegisterAdminForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
    
    def clean_age(self):
        age_value = self.cleaned_data['age']
        if age_value < 18:
            raise forms.ValidationError('Вы слишком молоды')
        
        return age_value


class ShopUserEditAdminForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
    
    def clean_age(self):
        age_value = self.cleaned_data['age']
        if age_value < 18:
            raise forms.ValidationError('Вы слишком молоды')
        
        return age_value


class CategoryEditAdminForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'image', 'short_description', 'full_description', 'price', 'stock')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''