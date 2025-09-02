from core.dados import Dados

def test_tirar_retorna_dos_valores():
    dados = Dados()
    valores = dados.tirar()
    assert len(valores) == 2
    assert all(1 <= v <= 6 for v in valores)

def test_obtener_valores_despues_de_tirada():
    dados = Dados()
    dados.tirar()
    valores = dados.obtener_valores()
    assert len(valores) == 2
    assert all(1 <= v <= 6 for v in valores)
