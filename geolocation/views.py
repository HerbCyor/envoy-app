from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .google_maps.addresses import (
    get_geolocation_from_address,
    random_addresses_from_central_geolocation,
    get_address_from_geolocation,
)

from .excel.writer import (
    create_standard_ee_csv,
    join_geolocation_address,
    create_geolocation_spreadsheet,
    create_standard_ee_spreadsheet,
    create_order_from_address,
)

from .excel.eemodel import (
    romaneio_distribution,
    EuentregoOrder,
)
from .excel.reader import (
    load_from_standard_ee_csv,
    load_from_geolocation_csv,
    load_geolocation_spreadsheet,
)

from django.conf import settings
from django.contrib import messages
from datetime import datetime
from .forms import UploadFileForm
from .models import FileRequest
from users.models import MyUser
import traceback


@login_required(login_url="login")
def geolocation(request):

    upload_file_form = UploadFileForm

    context = {
        "upload_file_form": upload_file_form,
    }

    return render(request, "geolocation.html", context)


@login_required(login_url="login")
def generate_points(request):

    if request.method == "POST":
        # get data from post
        try:
            latitude = float(request.POST.get("latitude"))
            longitude = float(request.POST.get("longitude"))
            radius = float(request.POST.get("radius"))
            quantity = int(request.POST.get("quantity"))
            romaneio = request.POST.get("romaneio")
            file_type = request.POST.get("file-type")
        except ValueError:
            messages.error(request, "Erro com os valores")
            return redirect("geolocation")

        # initialize orders creation

        order_list = []
        try:
            address_list = random_addresses_from_central_geolocation(
                quantity=quantity, center_coords=(latitude, longitude), radius=radius
            )
            for address in address_list:
                ee_order = create_order_from_address(
                    address=address, coords=(latitude, longitude)
                )
                ### shitty validation
                if isinstance(ee_order, EuentregoOrder):
                    order_list.append(ee_order)

            # ROMANEIO : adding romaneiro options
            if romaneio:
                order_list = romaneio_distribution(order_list)

            # handling file creation

            if file_type == "csv":
                output_file_name = datetime.now().strftime("%d%m%Y%H%M%S")
                file_path = create_standard_ee_csv(
                    filename=output_file_name, order_list=order_list
                )

                messages.success(request, "Arquivo csv criado com sucesso")
                return FileResponse(open(file_path, "rb"))

            elif file_type == "excel":
                wb = create_standard_ee_spreadsheet(order_list)

                output_file_name = datetime.now().strftime("%d%m%Y%H%M%S")
                file_path = f"{settings.MEDIA_ROOT}/files/{output_file_name}.xlsx"
                wb.save(file_path)

                messages.success(request, "Arquivo criado com sucesso")

                return FileResponse(open(file_path, "rb"))

        except Exception as e:
            messages.error(request, "Houve um erro com seu processo")
            print(e)

    return render(request, "geolocation.html")


def address_from_geolocation(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        #####BREAK THIS TRY/EXCEPT
        try:
            if form.is_valid():
                file = request.FILES.get("file")
                file_request = FileRequest(
                    user=MyUser.objects.get(id=request.user.id),
                    input_file=file,
                )
                file_request.save()
                # handle file and api calls here
                messages.success(request, "arquivo enviado com sucesso")

                input_file_name = file_request.input_file.path
                address_with_geolocation_list = []
                geolocation_list = []
                session_api_calls = 0
                ###excel

                if input_file_name.endswith(".xlsx"):
                    geolocation_list = load_geolocation_spreadsheet(
                        filename=input_file_name
                    )
                ###csv
                elif input_file_name.endswith(".csv"):

                    geolocation_list = load_from_geolocation_csv(input_file_name)

                else:
                    messages.error(request, "Extensão do arquivo não suportada")
                    return redirect("geolocation")

                qnt = len(geolocation_list)
                # len
                for i, geolocation in enumerate(geolocation_list):
                    address_dict = get_address_from_geolocation(
                        geolocation
                    )  # call api google
                    address_with_geolocation = join_geolocation_address(
                        address_dict, geolocation
                    )
                    address_with_geolocation_list.append(address_with_geolocation)
                    # send i >>>> Filerequest current_process
                    # save to database

                    print(f"{i}/{qnt} ---- {geolocation}")
                    session_api_calls += 1
                ###generate standard ee csv file
                output_file_name = datetime.now().strftime("%d%m%Y%H%M%S")
                file_path = create_geolocation_spreadsheet(
                    filename=output_file_name,
                    address_with_geolocation_list=address_with_geolocation_list,
                )

                messages.success(request, "Arquivo csv criado com sucesso")

                file_request.api_calls += session_api_calls
                file_request.save()
                return FileResponse(open(file_path, "rb"))

            else:
                print(form.is_valid)
        except Exception as e:
            print(e)
            traceback.print_exc()

        return redirect("geolocation")
    return redirect("geolocation")


def geolocation_from_address(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                file = request.FILES.get("file")
                file_request = FileRequest(
                    user=MyUser.objects.get(id=request.user.id),
                    input_file=file,
                )
                file_request.save()

                messages.success(request, "arquivo enviado com sucesso")
                ################ handle file and api calls here ########################

                input_file_name = file_request.input_file.path  # not url

                # load csv
                order_list = load_from_standard_ee_csv(input_file_name)
                # query google maps api
                session_api_calls = 0
                for order in order_list:
                    order_address = f"{order.endereco}, {order.numero} - {order.bairro} - {order.municipio}, {order.uf} - {order.cep}"
                    try:
                        result = get_geolocation_from_address(order_address)
                        order.latitude = str(result[0])
                        order.longitude = str(result[1])
                        print(result)
                        session_api_calls += 1
                        print(f"{session_api_calls} api calls")

                    except:
                        order.latitude, order.longitude = ("n/a", "n/a")
                # generate ee model csv
                output_file_name = datetime.now().strftime("%d%m%Y%H%M%S")
                file_path = create_standard_ee_csv(
                    filename=output_file_name, order_list=order_list
                )

                messages.success(request, "Arquivo csv criado com sucesso")

                file_request.api_calls += session_api_calls
                file_request.save()
                return FileResponse(open(file_path, "rb"))

        except Exception as e:
            print(e)

    return redirect("geolocation")
