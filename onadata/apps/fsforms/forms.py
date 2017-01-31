from django.forms.extras.widgets import SelectDateWidget
from django import forms
from django.utils.translation import ugettext_lazy as _
from onadata.apps.fieldsight.models import Site
from onadata.apps.logger.models import XForm
from .models import FieldSightXF, Stage, Schedule, FormGroup, FORM_STATUS


class AssignSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project', None)
        try:
            self.form_site = kwargs.get('instance').site.id
        except:
            self.form_site = 0
        super(AssignSettingsForm, self).__init__(*args, **kwargs)
        if self.project_id is not None:
            sites = Site.objects.filter(project__id=self.project_id).exclude(pk=self.form_site)
        else:
            sites = Site.objects.all()
        self.fields['site'].choices = [(obj.id, obj.name) for obj in sites]
        self.fields['site'].empty_label = None

    class Meta:
        fields = ['site']
        model = FieldSightXF


class FormTypeForm(forms.ModelForm):

    CHOICES = [(3, 'Normal Form'),
             (2, 'Schedule Form'),
            (1, 'Stage Form')]

    form_type = forms.ChoiceField(error_messages={'required': 'Please Choose Form Type !'},
                                  choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        fields = ['form_type']
        model = FieldSightXF


class FormStageDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormStageDetailsForm, self).__init__(*args, **kwargs)
        obj_list = Stage.objects.filter(stage__isnull=False, fieldsightxf__isnull=True)
        self.fields['stage'].choices = [(obj.id, obj.name) for obj in obj_list if not obj.form_exists()]
        self.fields['stage'].empty_label = None

    class Meta:
        fields = ['stage']
        model = FieldSightXF


class FormScheduleDetailsForm(forms.ModelForm):
    class Meta:
        fields = ['schedule']
        model = FieldSightXF


class FSFormForm(forms.ModelForm):

    class Meta:
        exclude = ['site']
        model = FieldSightXF


class StageForm(forms.ModelForm):

    class Meta:
        exclude = ['group', 'stage', 'site', 'shared_level', 'project', 'ready']
        model = Stage


class MainStageEditForm(forms.ModelForm):

    class Meta:
        exclude = ['group', 'stage', 'site', 'shared_level', 'project', 'ready', 'order']
        model = Stage


class SubStageEditForm(forms.ModelForm):
    forms_list = [(obj.id, obj.title) for obj in XForm.objects.all()]
    form = forms.ChoiceField(widget = forms.Select(),
                     choices = forms_list, required=False,)

    class Meta:
        exclude = ['group', 'stage', 'site', 'shared_level', 'project', 'ready', 'order']
        model = Stage


class AddSubSTageForm(forms.ModelForm):
    forms_list = [(obj.id, obj.title) for obj in XForm.objects.all()]
    form = forms.ChoiceField(widget = forms.Select(),
                     choices = forms_list, required=False,)
    class Meta:
        exclude = ['stage', 'group', 'shared_level', 'site', 'project', 'ready']
        model = Stage


class AssignFormToStageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignFormToStageForm, self).__init__(*args, **kwargs)
        xf_list = XForm.objects.all()
        self.fields['xf'].choices = [(f.id,f.title) for f in xf_list]
        self.fields['xf'].empty_label = None

    class Meta:
        fields = ['xf','site','is_staged','is_scheduled','stage']
        model = FieldSightXF
        labels = {
            "xf": _("Select Form"),
        }
        widgets = {'site': forms.HiddenInput(),
                   'is_staged': forms.HiddenInput(),
                   'is_scheduled': forms.HiddenInput(),
                   'stage': forms.HiddenInput()}


class AssignFormToScheduleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignFormToScheduleForm, self).__init__(*args, **kwargs)
        xf_list = XForm.objects.all()
        self.fields['xf'].choices = [(xf.id, xf.title) for xf in xf_list]
        self.fields['xf'].empty_label = None

    class Meta:
        fields = ['xf','site','is_staged','is_scheduled', 'schedule']
        model = FieldSightXF
        labels = {
            "xf": _("Select Form"),
        }
        widgets = {'site': forms.HiddenInput(),
                   'is_staged': forms.HiddenInput(),
                   'is_scheduled': forms.HiddenInput(),
                   'schedule': forms.HiddenInput()}

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')


class ScheduleForm(forms.ModelForm):
    forms_list = [(obj.id, obj.title) for obj in XForm.objects.all()]
    form = forms.ChoiceField(widget = forms.Select(),
                     choices = forms_list, required=False,)

    class Meta:
        exclude = ['site','project']
        model = Schedule
        widgets = { 'selected_days': forms.CheckboxSelectMultiple,
                    'date_range_start': SelectDateWidget,
                    'date_range_end': SelectDateWidget,
                    }


class GroupForm(forms.ModelForm):

    class Meta:
        exclude = ['creator']
        model = FormGroup


class AlterAnswerStatus(forms.Form):
    status = forms.ChoiceField(widget = forms.Select(),
                     choices = (FORM_STATUS), required = True,)

