from django.contrib import admin
from .models import (
    CostCenter, Department, GLAccount, MaterialGroup, Plant,
    PRApprovalAction, PRItem, PurchaseRequisition, PurchasingGroup, UnitOfMeasure,
)

for model in [Department, UnitOfMeasure, MaterialGroup, Plant, PurchasingGroup, CostCenter, GLAccount]:
    admin.site.register(model)


class PRItemInline(admin.TabularInline):
    model = PRItem
    extra = 0


class PRApprovalInline(admin.TabularInline):
    model = PRApprovalAction
    extra = 0
    readonly_fields = ('action', 'note', 'acted_by', 'acted_at')


@admin.register(PurchaseRequisition)
class PurchaseRequisitionAdmin(admin.ModelAdmin):
    list_display = ('pr_number', 'requestor', 'department', 'pr_type', 'status', 'created_at')
    inlines = [PRItemInline, PRApprovalInline]
