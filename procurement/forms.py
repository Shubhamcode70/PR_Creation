from django import forms
from django.forms import inlineformset_factory
from .models import PRApprovalAction, PRItem, PurchaseRequisition


class PurchaseRequisitionForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequisition
        fields = [
            'department', 'purpose_of_procurement', 'single_vendor_justification',
            'pr_type', 'cr_id', 'asset_number',
        ]


class PRItemForm(forms.ModelForm):
    class Meta:
        model = PRItem
        exclude = ['purchase_requisition', 'total_value']


class PRApprovalForm(forms.ModelForm):
    class Meta:
        model = PRApprovalAction
        fields = ['action', 'note']


PRItemFormSet = inlineformset_factory(
    PurchaseRequisition,
    PRItem,
    form=PRItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=100,
    validate_max=True,
)
