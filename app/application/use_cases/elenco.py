
from app.application.dtos.elenco import (
    CriarElencoDTO,
    AtualizarElencoDTO,
)
from app.domain.repositories.elenco_repository import ElencoRepository


class ElencoUseCases:
    def __init__(self, repository: ElencoRepository):
        self.repository = repository

    async def criar(self, dados: CriarElencoDTO):
        existente = await self.repository.list_elencos()

        if any(elenco.ano == dados.ano for elenco in existente):
            raise ValueError("Já existe um elenco cadastrado para esse ano.")

        return await self.repository.create_elenco(
            ano=dados.ano,
            status=dados.status,
        )

    async def listar(self):
        return await self.repository.list_elencos()

    async def buscar(self, elenco_id: int):
        elenco = await self.repository.get_elenco(elenco_id)

        if elenco is None:
            raise ValueError("Elenco não encontrado.")

        return elenco

    async def atualizar(self, dados: AtualizarElencoDTO):
        elenco = await self.buscar(dados.elenco_id)

        ano = dados.ano if dados.ano is not None else elenco.ano
        status = dados.status if dados.status is not None else elenco.status

        existentes = await self.repository.list_elencos()
        if any(
            item.id != dados.elenco_id and item.ano == ano
            for item in existentes
        ):
            raise ValueError("Já existe um elenco cadastrado para esse ano.")

        return await self.repository.update_elenco(
            elenco_id=dados.elenco_id,
            ano=ano,
            status=status,
        )

    async def excluir(self, elenco_id: int):
        await self.buscar(elenco_id)
        excluido = await self.repository.delete_elenco(elenco_id)

        if not excluido:
            raise ValueError("Não foi possível excluir o elenco.")

        return True
