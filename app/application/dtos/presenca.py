from dataclasses import dataclass


@dataclass
class CriarPresencaDTO:
    atleta_id: int
    treino_id: int
    confirmacao: bool | None = None
    presente: bool | None = None


@dataclass
class AtualizarConfirmacaoDTO:
    treino_id: int
    confirmacao: bool


@dataclass
class AtualizarPresenteDTO:
    atleta_id: int
    treino_id: int
    presente: bool