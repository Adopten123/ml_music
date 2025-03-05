"""Forms Module"""
from django import forms
from .models import Playlist, PlayerUser


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'logo', 'is_public', 'added_users', 'tracks']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'spotify-input',
                'placeholder': 'Название плейлиста'
            }),
            'logo': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'hidden-input'
            }),
            'added_users': forms.SelectMultiple(attrs={
                'class': 'spotify-select'
            }),
            'tracks': forms.CheckboxSelectMultiple(attrs={
                'class': 'track-select-container',
            }),
            'is_public': forms.Select(choices=Playlist.Status.choices)
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['logo'].required = False  # Поле необязательно
        if user:
            self.fields['added_users'].queryset = PlayerUser.objects.exclude(id=user.id)
            self.instance.owner = user  # Устанавливаем владельца

    def clean_name(self):
        name = self.cleaned_data['name']
        if Playlist.objects.filter(name=name, owner=self.instance.owner).exists():
            raise forms.ValidationError("У вас уже есть плейлист с таким названием")
        return name

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('tracks'):
            self.add_error('tracks', 'Выберите хотя бы один трек')
        return cleaned_data
