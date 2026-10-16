"""Testes da PRÁTICA 4 — três níveis de teste para um programa desktop.

   Nível A  lógica pura            -> rápido, o MAIS importante
   Nível B  interface com dublês   -> sem janela (Mock + patch)
   Nível C  janela real            -> lento, poucos, precisa de tela

Rode:  pytest -v          (sem o nível C: pytest -v -m "not gui")


"""
import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from app import AppConversor
from conversor import (
    celsius_para_fahrenheit,
    converter_texto,
    fahrenheit_para_celsius,
)


# ===========================================================================
# NÍVEL A — lógica pura (nenhuma janela envolvida)
# ===========================================================================
@pytest.mark.parametrize(
    ("celsius", "esperado"),
    [(0, 32), (100, 212), (-40, -40)],
)
def test_celsius_para_fahrenheit(celsius, esperado):
    assert celsius_para_fahrenheit(celsius) == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("fahrenheit", "esperado"),
    [(32, 0), (212, 100), (-40, -40)],
)
def test_fahrenheit_para_celsius(fahrenheit, esperado):
    assert fahrenheit_para_celsius(fahrenheit) == pytest.approx(esperado)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("100", "212.0 °F"), ("36,5", "97.7 °F"), ("0", "32.0 °F")],
)
def test_converter_texto(texto, esperado):
    assert converter_texto(texto) == esperado


@pytest.mark.parametrize(
    ("texto", "mensagem"),
    [
        ("abc", "Digite um número válido."),
        ("-273,16", "Temperatura abaixo do zero absoluto (-273,15 °C)."),
    ],
)
def test_converter_texto_invalido(texto, mensagem):
    with pytest.raises(ValueError) as erro:
        converter_texto(texto)
    assert str(erro.value) == mensagem


# ===========================================================================
# NÍVEL B — interface testada SEM abrir janela
#   AppConversor.__new__(AppConversor) cria o objeto PULANDO o __init__
#   (que abriria a janela). Depois trocamos os widgets por Mock: um
#   objeto "de mentira" que aceita qualquer chamada e a registra.
# ===========================================================================
def criar_app_sem_janela():
    app = AppConversor.__new__(AppConversor)
    app.entrada = Mock()
    app.rotulo = Mock()
    return app


def test_interface_mostra_resultado_da_conversao():
    app = criar_app_sem_janela()
    app.entrada.get.return_value = "100"

    app.converter()

    app.rotulo.config.assert_called_once_with(text="212.0 °F")


def test_interface_mostra_erro_e_limpa_resultado_invalido():
    app = criar_app_sem_janela()
    app.entrada.get.return_value = "abc"

    with patch("app.messagebox") as messagebox:
        app.converter()

    messagebox.showerror.assert_called_once_with(
        "Entrada inválida", "Digite um número válido."
    )
    app.rotulo.config.assert_called_once_with(text="—")


# ===========================================================================
# NÍVEL C — janela REAL. Usamos botao.invoke(), que executa o "command" do
# botão sem precisar do mainloop() (que travaria o teste).
# Em computador sem tela (servidor Linux) o teste é PULADO, não falha.
# ===========================================================================
@pytest.mark.gui
def test_janela_real_converte_ao_invocar_botao():
    try:
        app = AppConversor()
    except tk.TclError as erro:
        pytest.skip(f"Janela Tkinter indisponível: {erro}")

    try:
        app.entrada.insert(0, "100")
        app.botao.invoke()
        assert app.rotulo.cget("text") == "212.0 °F"
    finally:
        app.janela.destroy()