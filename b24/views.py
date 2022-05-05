from django.shortcuts import render
from .models import Partner, Region, DemoRequest
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import DemoForm
import random, requests, time, aiohttp
import asyncio
from asgiref.sync import sync_to_async


async def send_to_b24(webhook, payload):
    # r = requests.post(webhook + 'crm.lead.add', json=payload)
    # print('Сопрограмма завершена')
    # print(r.text)

    async with aiohttp.ClientSession() as session:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])
            print('Сопрограмма завершена')

# Create your views here.


def _get_num_partner():
    return Partner.objects.all().count()

def _get_num_region():
    return Region.objects.all().count()

def _get_demo_requests():
    return DemoRequest.objects.count()


async def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_partner = Partner.objects.all().count()
    num_region = Region.objects.all().count()
    # Available books (status = 'a')
    num_demo_requests = DemoRequest.objects.count()

    # num_partner = sync_to_async(_get_num_partner, thread_sensitive=True)
    # num_region = sync_to_async(_get_num_region, thread_sensitive=True)
    # num_demo_requests = sync_to_async(_get_demo_requests, thread_sensitive=True)

    context = {
        'num_partner': num_partner,
        'num_region': num_region,
        'num_demo_requests': num_demo_requests,
    }

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = DemoForm(request.POST)

        # chosen_partner = sync_to_async(random.choice(Partner.objects.filter(region__exact=form['region'].value())))
        chosen_partner = random.choice(Partner.objects.filter(region__exact=form['region'].value()))
        print(chosen_partner)

        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            f = form.save(commit=False)
            f.partner = chosen_partner
            f.save()

            if chosen_partner.webhook:
                print(chosen_partner.webhook)

                payload = {
                    "fields":
                        {
                            "TITLE": "Заявка по демодоступу ("+form['name'].value()+")",
                            "NAME": form['name'].value(),
                            "STATUS_ID": "NEW",
                            "OPENED": "Y",
                            "ASSIGNED_BY_ID": 1,
                            "COMMENTS": "Регион: "+form['region'].value(),
                            "PHONE": [{"VALUE": form['phone_number'].value(), "VALUE_TYPE": "WORK"}]
                        }}

                # r = requests.post(chosen_partner.webhook+'crm.lead.add', json=payload)
                # print(r.text)
                # await send_to_b24(chosen_partner.webhook, payload)
                task = asyncio.create_task(send_to_b24(chosen_partner.webhook, payload))
                # asyncio.run(send_to_b24(chosen_partner.webhook, payload))
                # task = asyncio.wait_for(send_to_b24(chosen_partner.webhook, payload), timeout=4)

                print('Сопрограмма запущена')

            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')
            # num_demo_requests = sync_to_async(DemoRequest.objects.count())
            num_demo_requests = DemoRequest.objects.count()
            context['num_demo_requests'] = num_demo_requests
            return render(request, 'thanks.html', context=context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DemoForm()

    context = {
        'num_partner': num_partner,
        'num_region': num_region,
        'num_demo_requests': num_demo_requests,
        'form': form,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
