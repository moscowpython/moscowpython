# -*- coding: utf-8 -*-
import codecs
from django.utils import simplejson
from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.json import DjangoJSONEncoder


class Serializer(JSONSerializer):
    def end_serialization(self):
        stream = codecs.getwriter('utf8')(self.stream)
        simplejson.dump(self.objects, stream, cls=DjangoJSONEncoder,
            ensure_ascii=False, **self.options)