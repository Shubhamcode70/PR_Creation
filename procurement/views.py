from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PRApprovalForm, PRItemFormSet, PurchaseRequisitionForm
from .models import PRApprovalAction, PurchaseRequisition


@login_required
def dashboard(request):
    prs = PurchaseRequisition.objects.filter(requestor=request.user).order_by('-created_at')
    return render(request, 'procurement/dashboard.html', {'prs': prs})


@login_required
def pr_create(request):
    if request.method == 'POST':
        form = PurchaseRequisitionForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.requestor = request.user
            pr.save()
            formset = PRItemFormSet(request.POST, instance=pr)
            if formset.is_valid():
                formset.save()
                if 'submit' in request.POST:
                    pr.status = PurchaseRequisition.Status.SUBMITTED
                    pr.save()
                return redirect('pr_detail', pk=pr.pk)
            pr.delete()
    else:
        form = PurchaseRequisitionForm()
        formset = PRItemFormSet()
    return render(request, 'procurement/pr_form.html', {'form': form, 'formset': formset})


@login_required
def pr_detail(request, pk):
    pr = get_object_or_404(PurchaseRequisition, pk=pk)
    can_approve = request.user.is_staff and pr.status == PurchaseRequisition.Status.SUBMITTED
    return render(request, 'procurement/pr_detail.html', {'pr': pr, 'can_approve': can_approve})


@user_passes_test(lambda u: u.is_staff)
def pr_approve(request, pk):
    pr = get_object_or_404(PurchaseRequisition, pk=pk, status=PurchaseRequisition.Status.SUBMITTED)
    if request.method == 'POST':
        form = PRApprovalForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.purchase_requisition = pr
            action.acted_by = request.user
            action.save()
            pr.status = PurchaseRequisition.Status.APPROVED if action.action == PRApprovalAction.Action.APPROVED else PurchaseRequisition.Status.REJECTED
            pr.save()
            return redirect('pr_detail', pk=pr.pk)
    else:
        form = PRApprovalForm()
    return render(request, 'procurement/pr_approve.html', {'pr': pr, 'form': form})
