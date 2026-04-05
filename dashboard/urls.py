from django.urls import path

from .views import (
    OverviewView,
    CategoryBreakdownView,
    MonthlyTrendsView,
    
    RecentActivityView,
    
)

urlpatterns = [
    path('overview/', OverviewView.as_view(), name='dashboard-overview'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='dashboard-category-breakdown'),
    path('monthly-trends/', MonthlyTrendsView.as_view(), name='dashboard-monthly-trends'),
    
    path('recent-activity/', RecentActivityView.as_view(), name='dashboard-recent-activity'),
    
    
]


