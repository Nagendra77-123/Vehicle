from django.shortcuts import render, get_object_or_404
from .models import Component, Vehicle, Issue, Payment
from django.http import JsonResponse

def register_component(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        is_new = request.POST.get('is_new') == 'on'
        component = Component.objects.create(name=name, price=price, is_new=is_new)
        return JsonResponse({'status': 'Component registered successfully'})
    return render(request, 'register_component.html')

def add_vehicle(request):
    if request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        model = request.POST.get('model')
        vehicle = Vehicle.objects.create(plate_number=plate_number, model=model)
        return JsonResponse({'status': 'Vehicle added successfully'})
    return render(request, 'add_vehicle.html')


def add_issue(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        component_id = request.POST.get('component_id')
        description = request.POST.get('description')
        repair_needed = request.POST.get('repair_needed') == 'on'

        if not component_id or not description:
            return JsonResponse({'status': 'Error', 'message': 'Component ID and description are required'}, status=400)

        try:
            component = get_object_or_404(Component, id=component_id)
            issue = Issue.objects.create(vehicle=vehicle, component=component, description=description,
                                         repair_needed=repair_needed)
            return JsonResponse({'status': 'success', 'message': 'Issue added successfully'})
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)

    return render(request, 'add_issue.html', {'vehicle': vehicle})


def calculate_price(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    issues = Issue.objects.filter(vehicle=vehicle)
    total_cost = sum(issue.component.price for issue in issues)
    Payment.objects.create(vehicle=vehicle, total_cost=total_cost, paid=False)
    return JsonResponse({'total_cost': total_cost})
