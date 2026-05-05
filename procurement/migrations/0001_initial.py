from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('name', models.CharField(max_length=100, unique=True)),('location', models.CharField(max_length=100))],
        ),
        migrations.CreateModel(
            name='GLAccount',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('code', models.CharField(max_length=20, unique=True)),('description', models.CharField(max_length=200))],
        ),
        migrations.CreateModel(
            name='MaterialGroup',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('code', models.CharField(max_length=20, unique=True)),('name', models.CharField(max_length=100))],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('code', models.CharField(max_length=20, unique=True)),('name', models.CharField(max_length=100))],
        ),
        migrations.CreateModel(
            name='PurchasingGroup',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('code', models.CharField(max_length=20, unique=True)),('name', models.CharField(max_length=100))],
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('code', models.CharField(max_length=20, unique=True)),('label', models.CharField(max_length=50))],
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('code', models.CharField(max_length=20, unique=True)),('name', models.CharField(max_length=100)),('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='procurement.department'))],
        ),
        migrations.CreateModel(
            name='PurchaseRequisition',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('pr_number', models.CharField(blank=True, max_length=20, unique=True)),('purpose_of_procurement', models.TextField()),('single_vendor_justification', models.TextField(blank=True)),('pr_type', models.CharField(choices=[('OPEX', 'OPEX'), ('CAPEX', 'CAPEX')], default='OPEX', max_length=10)),('cr_id', models.CharField(blank=True, max_length=50)),('asset_number', models.CharField(blank=True, max_length=50)),('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='DRAFT', max_length=12)),('created_at', models.DateTimeField(auto_now_add=True)),('updated_at', models.DateTimeField(auto_now=True)),('submitted_at', models.DateTimeField(blank=True, null=True)),('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='procurement.department')),('requestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))],
        ),
        migrations.CreateModel(
            name='PRItem',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('item_no', models.PositiveIntegerField()),('short_text', models.CharField(max_length=255)),('quantity', models.DecimalField(decimal_places=2, max_digits=12)),('valuation_price', models.DecimalField(decimal_places=2, max_digits=12)),('total_value', models.DecimalField(decimal_places=2, default=0, max_digits=14)),('delivery_date', models.DateField()),('requisitioner', models.CharField(max_length=100)),('acct_qty', models.DecimalField(decimal_places=2, max_digits=12)),('asset_code', models.CharField(blank=True, max_length=50)),('cost_bearer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cost_bearer_items', to='procurement.costcenter')),('cost_center', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cost_center_items', to='procurement.costcenter')),('gl_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='procurement.glaccount')),('material_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='procurement.materialgroup')),('plant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='procurement.plant')),('purchase_requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='procurement.purchaserequisition')),('purchasing_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='procurement.purchasinggroup')),('uom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='procurement.unitofmeasure'))],
            options={'ordering': ['item_no'], 'unique_together': {('purchase_requisition', 'item_no')}},
        ),
        migrations.CreateModel(
            name='PRApprovalAction',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('action', models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], max_length=10)),('note', models.TextField()),('acted_at', models.DateTimeField(auto_now_add=True)),('acted_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),('purchase_requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_actions', to='procurement.purchaserequisition'))],
            options={'ordering': ['-acted_at']},
        ),
    ]
