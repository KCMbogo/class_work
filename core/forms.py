from django import forms
from core.models import Review


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, initial=1, 
        widget=forms.HiddenInput(attrs={'id': 'product-quanity'}
    ))
    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'product', 'rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...', 'rows': 5}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'rating': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})

