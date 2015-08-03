from django import forms
import mailator.models as model

class EmailTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailTypeForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'exclude_members' and f != 'use_bcc':
                self.fields[f].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = model.Type
        fields = ('name', 'description', 'email_from', 'reply_to', 'layout', 'category', 'connection', 'use_bcc', 'exclude_members')


class TemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs = {'class': 'form-control'}
        self.fields['html_content'].widget.attrs = {'class': 'form-control', 'rows': '10'}

    class Meta:
        model = model.Template
        fields = ('subject', 'html_content', 'attachment', 'attachment_2')


class EmailListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailListForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control'}
        self.fields['format'].widget.attrs = {'class': 'form-control'}
        self.fields['sep'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = model.EmailList
        fields = ('name', 'format', 'sep')


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'exclude_members':
                self.fields[f].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = model.Task
        fields = ('name', 'lang', 'email', 'liste', 'connection_override', 'from_override', 'step', 'growth', 'schedule', 'concurrency', 'exclude_members')

class UploadListeForm(forms.Form):
    file = forms.FileField()
