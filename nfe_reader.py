import re
import sys
import csv
import os.path
import pandas as pd
import xml.etree.ElementTree as ET
from textual.app import App
from textual.widgets import Header, Footer, Input, Label
from textual_pandas.widgets import DataFrameTable


nfe = ""
class NFEApp(App):
    TITLE = "NF-e XML Reader"
    BINDINGS = [("escape", "quit", "Exit")]
    def compose(self):
        yield Header()
        self.label = Label("")
        yield self.label
        yield Input(placeholder="Type a NF-e: ", id="nfe")
        yield DataFrameTable()
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted):
        global nfe
        nfe_input = self.query_one("#nfe", Input)
        nfe = nfe_input.value
        main()
        global name_file
        if os.path.isfile(f"{name_file}.csv"):
            self.label.update("Successfully csv file created")
        global table
        table_ = self.query_one(DataFrameTable)
        table_.add_df(table)

    def action_quit(self) -> None:
        self.exit()


def main():
    global nfe
    global name_file
    nfe = nfe.strip()
    name_file = nfe.split(".")[0]
    validate(nfe)
    data = format(parser(nfe))
    exporter([data], name_file)
    grafics(name_file)


def validate(n):
    if not re.search(r"\.xml", n):
        sys.exit("It's not a NF-e.")
    try:
        readable = ET.parse(n)
    except FileNotFoundError:
        sys.exit("File Not Found.")


def parser(n):
    entered_nfe = ET.parse(n)
    root = entered_nfe.getroot()
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    ide = root.find(".//ns:ide", ns)
    emit = root.find(".//ns:emit", ns)
    dest = root.find(".//ns:dest", ns)
    prod = root.find(".//ns:prod", ns)
    total = root.find(".//ns:ICMSTot", ns)

    data = {
        "UF": ide.find("ns:cUF", ns).text,
        "Número": ide.find("ns:nNF", ns).text,
        "Emissão": ide.find("ns:dhEmi", ns).text,
        "Emitente": emit.find("ns:xNome", ns).text,
        "CNPJ": emit.find("ns:CNPJ", ns).text,
        "CPF": dest.find("ns:CPF", ns).text,
        "Produto": prod.find("ns:xProd", ns).text,
        "Quantidade": prod.find("ns:qCom", ns).text,
        "Valor Unitário": prod.find("ns:vUnCom", ns).text,
        "Valor Total": total.find("ns:vNF", ns).text,
    }

    return data


def format(d):
    cuf = {
        11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO", 21: "MA", 22: "PI",
        23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA", 31: "MG", 32: "ES",
        33: "RJ", 35: "SP", 41: "PR", 42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF",
    }
    d["UF"] = cuf[int(d["UF"])]

    data_e = d["Emissão"]
    d["Emissão"] = f"{data_e[8:10]}/{data_e[5:7]}/{data_e[0:4]}"

    cnpj = d["CNPJ"]
    d["CNPJ"] = f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

    cpf = d["CPF"]
    d["CPF"] = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    valor_un = d["Valor Unitário"].split(".")
    d["Valor Unitário"] = f"R${valor_un[0]},{valor_un[1]}"

    valor_total = d["Valor Total"].split(".")
    d["Valor Total"] = f"R${valor_total[0]},{valor_total[1]}"

    return d


def exporter(d, n):
    keys = d[0].keys()
    with open(f"{n}.csv", "w", newline="", encoding="utf-8") as c:
        writer = csv.DictWriter(c, fieldnames=keys)
        writer.writeheader()
        writer.writerows(d)


def grafics(n):
    global table
    table = pd.read_csv(f"{n}.csv")


if __name__ == "__main__":
    app = NFEApp()
    app.run()

