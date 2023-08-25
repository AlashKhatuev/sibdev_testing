from rest_framework.parsers import MultiPartParser, ParseError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
import csv
import pytz
import codecs
import datetime
from .models import Entry
from django.db.models import Sum
from itertools import groupby 
from collections import Counter

class FileUpload(APIView):
    parser_classes=(MultiPartParser,)

    def post(self, request: Request, format=None) -> Response:
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']
        rows = csv.DictReader(codecs.iterdecode(file, 'utf-8'))
        entries = []
        for row in rows:
            print(row["customer"])
            row["date"] = pytz.utc.localize(datetime.datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S.%f"))
            entries.append(Entry(**row))
            print(entries[-1].quantity)
        
        Entry.objects.bulk_create(entries)

        return Response(data={"message": "all's ok"}, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        query = Entry.objects.values("customer", "item").annotate(totals=Sum('total')).order_by("-customer")
        result = []
        for key, group in groupby(query, lambda x: x['customer']):
            data = {'username': key, 'spent_money': 0, 'gems': set()}
            for item in group:
                data['spent_money'] += item['totals']
                data['gems'].add(item['item'])
            result.append(data)
        result.sort(key=lambda x:x['spent_money'], reverse=True)
        result = result[:5]
        counter = Counter()
        for item in result:
            counter.update(Counter(item['gems']))

        for item in result:
            item['gems'] = [gem for gem in item['gems'] if counter.get(gem, 0) > 1]
        return Response(result)