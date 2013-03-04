from django import forms
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.core.serializers.json import DjangoJSONEncoder

from models import Configuration


class ConfigurationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key')
        self.configuration = kwargs.pop('configuration')
        self.instance = args[0]
        super(ConfigurationForm, self).__init__(*args, **kwargs)
        if self.instance:
            initial = self.instance
            # model based fields don't know what to due with objects,
            # but they do know what to do with pks
            for key, value in initial.items():
                if hasattr(value, 'pk'):
                    initial[key] = value.pk
            self.initial.update(initial)

    def save(self):
        data = dict(self.cleaned_data)
        del data['site']
        return self.configuration.set_config(data)

    def config_task(self):
        return "No configuration action defined for %s" % self.key

    class Meta:
        model = Configuration
        fields = ['site']


# class EncryptedConfigurationForm(ConfigurationForm):
#
#     def save(self, commit=True):
#         instance = super(EncryptedConfigurationForm, self).save(commit=False)
#         data = instance.get_data()
#         instance.is_crypto = True
#         instance.set_data(data)
#         if commit:
#             instance.save()
#         return instance