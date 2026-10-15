"""Testes da PRÁTICA 1 — conceitos: AAA, approx, raises e parametrize.

Como rodar (dentro desta pasta):   pytest -v
"""

# Usando ferramenta de Testes
import pytest
from boletim import calcular_media, situacao

# ---------------------------------------------------------------------------
# 1) PRIMEIRO TESTE — padrão AAA (Arrange, Act, Assert)
#    O pytest só enxerga funções cujo nome começa com "test_".
# ---------------------------------------------------------------------------

def test_media_de_duas_notas():
    # Arrange (Preparar) - Dados de entrada
    notas = [6, 8]

    # Act (Agir) - Chamar a função
    media = calcular_media(notas)

    # Assert (Afirmar) - Conferir o resultado
    assert media == 7.0
# ---------------------------------------------------------------------------
# 2) NÚMEROS DECIMAIS — nunca compare float com "==".
#    Em computadores, 0.1 + 0.2 vale 0.30000000000000004. O pytest.approx
#    compara "quase igual" (com uma tolerância minúscula).
# ---------------------------------------------------------------------------

def test_media_com_decimais_usa_approx():
    assert calcular_media([0.1, 0.2]) == pytest.approx(0.3)

# ---------------------------------------------------------------------------
# 3) TESTES NEGATIVOS — o código deve RECUSAR entradas inválidas.
#    pytest.raises passa se a exceção acontecer e falha se NÃO acontecer.
#    "match" confere um pedaço da mensagem de erro (expressão regular).
# ---------------------------------------------------------------------------

def test_lista_vazia_levanta_erro():
    with pytest.raises(ValueError, match="Lista de notas vazia"):
        calcular_media([])

# ---------------------------------------------------------------------------
# 4) PARAMETRIZE — mesma lógica, várias entradas, UMA função.
#    Cada valor da lista vira um teste separado no relatório.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("nota_invalida", [-0.1, 10.1, 100])
def test_nota_fora_do_intervalo_levanta_erro(nota_invalida):
    with pytest.raises(ValueError, match="entre 0 e 10"):
        calcular_media([7, nota_invalida])
# ---------------------------------------------------------------------------
# 5) VALOR LIMITE (borda) — a maioria dos bugs mora na fronteira.
#    Regra: >= 6 aprova; >= 4 recuperação. Testamos o valor exato da
#    fronteira e o vizinho logo abaixo dela.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "media, esperado",
    [
        (10.0, "Aprovado"),
        (6.0, "Aprovado"),
        (5.9, "Recuperação"),
        (4.0, "Recuperação"),
        (3.9, "Reprovado"),
        (0.0, "Reprovado"),
    ],
)
def test_situacao_nas_bordas(media, esperado):
    assert situacao(media) == esperado

# ---------------------------------------------------------------------------
# 6) TESTE DE INTEGRAÇÃO PEQUENO — as duas funções juntas.
#    (5 + 7) / 2 = 6.0, justo na borda de aprovação.
# ---------------------------------------------------------------------------

def test_fluxo_completo_media_e_situacao():
    # Arrange (Preparar) - Notas cuja média fica exatamente no limite de aprovação
    notas = [5, 7]

    # Act (Agir) - Calcular a média e a situação
    media = calcular_media(notas)
    resultado = situacao(media)

    # Assert (Afirmar) - Conferir a situação final
    assert resultado == "Aprovado"
