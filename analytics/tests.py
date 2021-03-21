from django.test import TestCase
from analytics.vars import *
from analytics.queries import *

# Create your tests here.
class QueryTestCase(TestCase):
    def setUp(self):
        print("here")
        return super().setUp()
    
    def query_test(self):
        queryset = get_model_raw_data_query(Fund,FUNDS_RAW_DATA_FIELDS)
        print(queryset.query)