from django import forms
from .models import Group, Event, Comment


class GroupForm(forms.ModelForm):
    tag = forms.CharField(label='Tag(comma separated list of tags)', max_length=255, required=False)

    class Meta:
        model = Group
        fields = ["name", "description", "thumbnail"]
        widgets = {
            "description": forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Group name',
            'description': 'Description',
            'thumbnail': 'Thumbnail',
        }

    def clean_tag(self):
        tag = self.cleaned_data.get("tag")
        tag_list = tag.split(",")
        return tag_list


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", 'address', "thumbnail", "held_date"]
        widgets = {
            "description": forms.Textarea(attrs={'rows': 3}),
            "held_date": forms.SelectDateWidget,
        }
        labels = {
            "name": "Event name",
            "description": "Description",
            "thumbnail": "Thumbnail",
            "held_date": "event_date",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", ]