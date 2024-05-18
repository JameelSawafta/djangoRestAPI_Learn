from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpensesSerializer
from .models import Expense


# Create your views here.

class ExpensesList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpensesSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Expense.objects.filter(owner = self.request.user)

class ExpenseDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpensesSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Expense.objects.filter(owner = self.request.user)



