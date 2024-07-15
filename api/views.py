from datetime import datetime
import requests

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import BondPost
from .serializers import BondPostSerializer


def isin_validator(isin: str) -> bool:
    '''
    '''

    ISIN_VALID = 'https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin={}'
    EXPECTED = 'vydaneisiny'

    valid_result = False

    response = dict(requests.get(ISIN_VALID.format(isin)).json())

    if EXPECTED in response.keys():
        valid_result = True
    
    return valid_result


@api_view(['GET'])
def view_bonds(request):
    '''List all bonds.'''

    bonds = BondPost.objects.all()
    
    if bonds:
        serializer = BondPostSerializer(bonds, many=True)
        requested_data = {
            'Bonds': serializer.data
        }
        return JsonResponse(requested_data)
    else:
        return Response('No data to show', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_bond(request):
    '''
    Create a new bond instance. Bond is validade by its ISIN.
    '''

    serializer = BondPostSerializer(data=request.data)

    if serializer.is_valid():
        isin = serializer.validated_data.get('isin')
        is_isin_valid = isin_validator(isin)

        if is_isin_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Invalid ISIN', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def manage_bond(request, isin):
    '''
    Retrieve, update, or delete a bond instance.
    Parameter: isin
    '''

    try:
        bond = BondPost.objects.get(isin=isin)
    except BondPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BondPostSerializer(bond)
        requested_data = {
            'Bond': serializer.data
        }
        return JsonResponse(requested_data)
    elif request.method == 'PUT':
        serializer = BondPostSerializer(bond, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        bond.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def bond_analyzer(request):
    '''
    Calculate statistic of whole set of bonds.
    Output: json
      avg_interest_rate - Average interest rate of all bonds.
      shortest_due_date - The bond that will be closest to maturity.
      total_bond_value  - Total portfolio value.
      future_bond_value - Future value of the portfolio.
    '''

    bonds = BondPost.objects.all()
 
    if bonds:
        serializer = BondPostSerializer(bonds, many=True)
        analyzer_data = {
            "avg_interest_rate": 0.0,
            "shortest_due_date": {},
            "total_bond_value": 0,
            "future_bond_value": 0
        }
        for bond_data in serializer.data:

            if analyzer_data['avg_interest_rate'] > 0:
                analyzer_data['avg_interest_rate'] = (analyzer_data['avg_interest_rate'] + bond_data['interest_rate']) / 2
            else:
                analyzer_data['avg_interest_rate'] = bond_data['interest_rate']
            
            if 'due_date' not in analyzer_data['shortest_due_date'].keys():
                analyzer_data['shortest_due_date'] = { 'due_date': bond_data['due_date'], 'isin': bond_data['isin'] }
            else:
                date_min = datetime.fromisoformat(analyzer_data['shortest_due_date']['due_date'][:-1] + '+00:00')
                date_min_new = datetime.fromisoformat(bond_data['due_date'][:-1] + '+00:00')
                if date_min_new < date_min:
                    analyzer_data['shortest_due_date'] = { 'due_date': bond_data['due_date'], 'isin': bond_data['isin'] }
            
            analyzer_data['total_bond_value'] += bond_data['bond_value']

            purchase_date = datetime.fromisoformat(bond_data['purchase_date'][:-1] + '+00:00')
            due_date = datetime.fromisoformat(bond_data['due_date'][:-1] + '+00:00')
            interest_period = due_date - purchase_date
            profit = (interest_period.days / bond_data['yields_freq']) * (bond_data['bond_value'] * bond_data['interest_rate'])
            total = bond_data['bond_value'] + profit
            analyzer_data['future_bond_value'] += total

        requested_data = {
            'Statistic': analyzer_data
        }

        return JsonResponse(requested_data)

