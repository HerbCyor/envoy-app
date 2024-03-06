from dataclasses import dataclass
import math
import random
import string


def random_license_plate():

    plate = []
    for _ in range(3):
        plate.append(
            string.ascii_uppercase[random.randint(0, len(string.ascii_uppercase) - 1)]
        )

    for _ in range(3):
        plate.append(string.digits[random.randint(0, len(string.digits) - 1)])
    return "".join(plate)


def random_cpf():
    cpf = [random.randint(0, 9) for _ in range(11)]

    return "%s%s%s.%s%s%s.%s%s%s-%s%s" % tuple(cpf)


def random_destinatario():
    return f"{name_list[random.randint(0,len(name_list)-1)]} {surname_list[random.randint(0,len(surname_list)-1)]}"  # nome aleatorio


def romaneio_distribution(order_list):
    n = len(order_list)
    qnt_order_per_romaneio = (n * math.ceil(-0.03 * n + 21.4)) / 100
    romaneio_value = 0
    new_order_list = []
    license_plate = ""
    for i, order in enumerate(order_list):
        if i % qnt_order_per_romaneio == 0:
            romaneio_value += 1
            license_plate = random_license_plate()
        order.romaneio = romaneio_value
        order.placa = license_plate
        new_order_list.append(order)
        # to do placa
    return new_order_list


headers = [
    "Loja",
    "Pedido",
    "Tipo (E/C)",
    "CPF/CNPJ",
    "Razao Social",
    "Nome",
    "Destinatario",
    "Telefone",
    "UF",
    "Municipio",
    "Bairro",
    "Numero",
    "Endereco",
    "CEP",
    "Latitude",
    "Longitude",
    "Complemento",
    "Janela Ini",
    "Janela Fim",
    "DT Lim",
    "Carga (KG)",
    "Carga (CM3)",
    "Nota",
    "Ano",
    "Mes",
    "Serie",
    "Cod. Carga",
    "Data Carga",
    "Romaneio",
    "Placa",
    "Data Romaneio",
    "Quantidade de Volumes",
    "Tag",
]
name_list = [
    "Carlos",
    "João",
    "Mateus",
    "Amanda",
    "Cíntia",
    "Felipe",
    "Adamastor",
    "Bruno",
    "Pâmela",
    "Patrícia",
    "Valder",
    "Célio",
    "Ivan",
    "Alberto",
    "Jonas",
    "Fernanda",
    "Fernando",
    "Caetano",
]
surname_list = [
    "dos Santos",
    "Pereira",
    "Martins",
    "Carvalho",
    "Cantoneiro",
    "Maciel",
    "Alcorta",
    "Fernandes",
    "Silva",
    "Matos",
    "Loureiro",
    "Veloso",
    "Hendel",
    "Giorgio",
    "Mendes",
    "Ventura",
]


@dataclass
class EuentregoOrder:
    loja: str = "Envoy"
    pedido: int = 1  # random 7digits
    tipo: str = "E"
    cpf_cnpj: str = ""
    razao_social: str = ""
    nome: str = ""
    destinatario: str = ""
    telefone: str = ""
    uf: str = ""
    municipio: str = ""
    bairro: str = ""
    numero: str = ""
    endereco: str = ""
    cep: str = ""
    latitude: str = ""
    longitude: str = ""
    complemento: str = ""
    janela_ini: str = ""
    janela_fim: str = ""
    dt_lim: str = ""  # datetime.today
    carga_kg: int = 1  # random 1~20
    carga_cm3: int = 1  # 50 ~500.000
    nota: str = ""
    ano: str = ""
    mes: str = ""
    serie: str = ""
    cod_carga: str = ""
    data_carga: str = ""
    romaneio: str = ""
    placa: str = ""  # mesma placa
    data_romaneio: str = ""
    qtd_volumes: int = 1  # random 1~10
    tag: str = ""
