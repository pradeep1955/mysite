from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from mystocks.utils import fetch_and_store_if_needed

from .forms import HoldingForm
from .models import Holding


@login_required
def portfolio_dashboard(request):
    holdings = Holding.objects.filter(user=request.user)

    portfolio_data = []
    total_investment = 0
    total_current_value = 0

    for holding in holdings:
        stock_data = fetch_and_store_if_needed(holding.symbol)

        close_price_float = stock_data.close if stock_data and stock_data.close else 0
        current_price = Decimal(str(close_price_float))

        current_value = holding.quantity * current_price
        investment_value = holding.quantity * holding.purchase_price
        gain_loss = current_value - investment_value

        percent_gain_loss = 0
        if investment_value > 0:
            percent_gain_loss = (gain_loss / investment_value) * 100

        portfolio_data.append(
            {
                "holding": holding,
                "current_price": current_price,
                "current_value": current_value,
                "gain_loss": gain_loss,
                "percent_gain_loss": percent_gain_loss,
            }
        )

        total_investment += investment_value
        total_current_value += current_value

    overall_gain_loss = total_current_value - total_investment
    overall_percent_gain_loss = 0
    if total_investment > 0:
        overall_percent_gain_loss = (overall_gain_loss / total_investment) * 100

    context = {
        "portfolio_data": portfolio_data,
        "total_investment": total_investment,
        "total_current_value": total_current_value,
        "overall_gain_loss": overall_gain_loss,
        "overall_percent_gain_loss": overall_percent_gain_loss,
    }
    return render(request, "portfolio/dashboard.html", context)


@login_required
def add_holding(request):
    if request.method == "POST":
        form = HoldingForm(request.POST)
        if form.is_valid():
            holding = form.save(commit=False)
            holding.user = request.user
            holding.save()
            return redirect("portfolio:dashboard")
    else:
        form = HoldingForm()

    return render(request, "portfolio/holding_form.html", {"form": form, "action": "Add"})


@login_required
def edit_holding(request, pk):
    holding = get_object_or_404(Holding, pk=pk, user=request.user)

    if request.method == "POST":
        form = HoldingForm(request.POST, instance=holding)
        if form.is_valid():
            form.save()
            return redirect("portfolio:dashboard")
    else:
        form = HoldingForm(instance=holding)

    return render(request, "portfolio/holding_form.html", {"form": form, "action": "Edit"})


@login_required
def delete_holding(request, pk):
    holding = get_object_or_404(Holding, pk=pk, user=request.user)

    if request.method == "POST":
        holding.delete()
        return redirect("portfolio:dashboard")

    return render(request, "portfolio/holding_confirm_delete.html", {"holding": holding})
