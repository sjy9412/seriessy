from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        max_length=200, 
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '한줄평을 입력해주세요 ( 하나만 입력 가능합니다 )',
            }
        )
    )
    score = forms.IntegerField(
        label='',
        widget=forms.NumberInput(
            attrs={
                'min': 0,
                'max': 10,
                'placeholder': '0 ~ 10점 까지 입력해주세요'
            }
        )
    )
    class Meta:
        model = Review
        fields = ('content', 'score')
