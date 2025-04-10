import pytest
from nfe_reader import validate, parser, format

def main():
    test_validate()
    test_parser()
    test_format()

def test_validate():
    with pytest.raises(SystemExit) as test1:
        validate("notexist.xml")
    assert test1.type == SystemExit
    assert test1.value.code == "Arquivo não encontrado."
    with pytest.raises(SystemExit) as test2:
        validate("not_a_file")
    assert test2.type == SystemExit
    assert test2.value.code == "Não é uma NF-e."

def test_parser():
    result = parser("nota1.xml")

    assert result["UF"] == "35"
    assert result["Número"] == "1001"
    assert result["Emissão"] == "2024-03-10T10:00:00-03:00"
    assert result["Emitente"] == "Comercial São José LTDA"
    assert result["CNPJ"] == "11222333000181"
    assert result["CPF"] == "12345678901"
    assert result["Produto"] == "Café em pó 500g"
    assert result["Quantidade"] == "1.0000"
    assert result["Valor Unitário"] == "9.50"
    assert result["Valor Total"] == "9.50"

def test_format():
    data = {
        "UF": "35",
        "Número": "123456",
        "Emissão": "2025-04-07T14:30:00-03:00",
        "Emitente": "Empresa Exemplo",
        "CNPJ": "12345678000199",
        "CPF": "98765432100",
        "Produto": "Produto Teste",
        "Quantidade": "2.0000",
        "Valor Unitário": "10.50",
        "Valor Total": "21.00",
    }

    result = format(data)

    assert result["UF"] == "SP"
    assert result["Emissão"] == "07/04/2025"
    assert result["CNPJ"] == "12.345.678/0001-99"
    assert result["CPF"] == "987.654.321-00"
    assert result["Valor Unitário"] == "R$10,50"
    assert result["Valor Total"] == "R$21,00"
    assert result["Emitente"] == "Empresa Exemplo"
    assert result["Produto"] == "Produto Teste"
