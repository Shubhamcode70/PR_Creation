from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.location})"


class UnitOfMeasure(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class MaterialGroup(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Plant(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class PurchasingGroup(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class CostCenter(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class GLAccount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} - {self.description}"


class PurchaseRequisition(models.Model):
    class PRType(models.TextChoices):
        OPEX = 'OPEX', 'OPEX'
        CAPEX = 'CAPEX', 'CAPEX'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    pr_number = models.CharField(max_length=20, unique=True, blank=True)
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    purpose_of_procurement = models.TextField()
    single_vendor_justification = models.TextField(blank=True)
    pr_type = models.CharField(max_length=10, choices=PRType.choices, default=PRType.OPEX)
    cr_id = models.CharField(max_length=50, blank=True)
    asset_number = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.pr_type == self.PRType.CAPEX and (not self.cr_id or not self.asset_number):
            raise ValidationError('CAPEX PR requires CR ID and Asset Number.')

    def save(self, *args, **kwargs):
        if not self.pr_number:
            year = timezone.now().year
            last_id = PurchaseRequisition.objects.filter(pr_number__startswith=f"PR-{year}-").aggregate(Max('id'))['id__max'] or 0
            self.pr_number = f"PR-{year}-{last_id + 1:04d}"
        if self.status == self.Status.SUBMITTED and self.submitted_at is None:
            self.submitted_at = timezone.now()
        super().save(*args, **kwargs)


class PRItem(models.Model):
    purchase_requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE, related_name='items')
    item_no = models.PositiveIntegerField()
    short_text = models.CharField(max_length=255)
    uom = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    valuation_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_value = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    delivery_date = models.DateField()
    material_group = models.ForeignKey(MaterialGroup, on_delete=models.PROTECT)
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)
    purchasing_group = models.ForeignKey(PurchasingGroup, on_delete=models.PROTECT)
    requisitioner = models.CharField(max_length=100)
    acct_qty = models.DecimalField(max_digits=12, decimal_places=2)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT, related_name='cost_center_items')
    gl_account = models.ForeignKey(GLAccount, on_delete=models.PROTECT)
    cost_bearer = models.ForeignKey(CostCenter, on_delete=models.PROTECT, related_name='cost_bearer_items', null=True, blank=True)
    asset_code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['item_no']
        unique_together = ('purchase_requisition', 'item_no')

    def clean(self):
        if self.purchase_requisition.pr_type == PurchaseRequisition.PRType.CAPEX and not self.asset_code:
            raise ValidationError('Asset code is required for CAPEX item.')

    def save(self, *args, **kwargs):
        self.total_value = self.quantity * self.valuation_price
        super().save(*args, **kwargs)


class PRApprovalAction(models.Model):
    class Action(models.TextChoices):
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    purchase_requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE, related_name='approval_actions')
    action = models.CharField(max_length=10, choices=Action.choices)
    note = models.TextField()
    acted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    acted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-acted_at']
