# -*- coding: utf-8 -*-
from django.core.serializers import pyyaml
from django.core.serializers.pyyaml import DjangoSafeDumper
import yaml


class Serializer(pyyaml.Serializer):

    def end_serialization(self):
        yaml.dump(self.objects, self.stream, Dumper=DjangoSafeDumper, allow_unicode=True, **self.options)