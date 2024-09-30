from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Product, ProductType, Category

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount', 'description', 'image', 'product_type', 'category']
        widgets = {
            'category': forms.Select(attrs={'disabled': 'disabled'}),  # Initially disabled
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()

        if 'product_type' in self.data:
            try:
                product_type_id = int(self.data.get('product_type'))
                self.fields['category'].queryset = Category.objects.filter(product_type_id=product_type_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input; ignore and leave category empty
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.product_type.categories.order_by('name')