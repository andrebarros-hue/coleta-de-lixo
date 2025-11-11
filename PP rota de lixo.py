import random
import time


# Factory: realiza a criação dos caminhões

class Caminhao:
    def __init__(self, tipo, prioridade):
        self.tipo = tipo
        self.prioridade = prioridade
        self.status = "Aguardando rota"
        self.coletas = 0  # usado para o relatório

    def coletar(self, rota):
        self.coletas += 1
        print(f"{self.tipo} está coletando lixo em {rota} (Prioridade: {self.prioridade}).")


class CaminhaoComum(Caminhao):
    def __init__(self):
        super().__init__("Caminhão Comum", "Baixa")


class CaminhaoReciclavel(Caminhao):
    def __init__(self):
        super().__init__("Caminhão Reciclável", "Média")


class CaminhaoHospitalar(Caminhao):
    def __init__(self):
        super().__init__("Caminhão Hospitalar", "Alta")


class CaminhaoFactory:
    @staticmethod
    def criar_caminhao(tipo):
        if tipo == "comum":
            return CaminhaoComum()
        elif tipo == "reciclavel":
            return CaminhaoReciclavel()
        elif tipo == "hospitalar":
            return CaminhaoHospitalar()
        else:
            raise ValueError("Tipo de caminhão inválido")



# Mediator: realiza a Torre de Comunicação

class TorreComunicacao:
    def __init__(self):
        self.historico = []
        self.alertas_enviados = 0

    def enviar_mensagem(self, caminhao, mensagem):
        registro = f"Torre -> {caminhao.tipo}: {mensagem}"
        self.historico.append(registro)
        print(registro)

    def enviar_alerta(self):
        alertas = [
            "Chuva intensa",
            "Acidente na via",
            "Bloqueio temporário",
            "Trânsito pesado",
            "Operação normal"
        ]
        alerta = random.choice(alertas)
        self.alertas_enviados += 1
        print(f"\nAlerta da Torre: {alerta}")
        return alerta



# Observer: observa os caminhões e suas rotas

class CaminhaoObserver:
    def __init__(self, caminhao, torre):
        self.caminhao = caminhao
        self.torre = torre

    def atualizar(self, nova_rota):
        self.caminhao.status = "Em rota"
        self.torre.enviar_mensagem(self.caminhao, f"Nova rota atribuída: {nova_rota}")
        self.caminhao.coletar(nova_rota)



# Rota: gerencia rotas e notifica caminhões

class RotaLixo:
    def __init__(self, torre):
        self.torre = torre
        self.observadores = []
        self.rotas = ["Zona Norte", "Zona Leste", "Centro", "Zona Sul", "Zona Oeste"]
        self.rota_atual = random.choice(self.rotas)

    def adicionar_observador(self, caminhao):
        self.observadores.append(caminhao)

    def notificar_observadores(self):
        # Ordena por prioridade antes de notificar
        ordem = {"Alta": 1, "Média": 2, "Baixa": 3}
        self.observadores.sort(key=lambda o: ordem[o.caminhao.prioridade])

        print("\nOrdem de saída dos caminhões:")
        for obs in self.observadores:
            print(f" - {obs.caminhao.tipo} (Prioridade: {obs.caminhao.prioridade})")

        for obs in self.observadores:
            obs.atualizar(self.rota_atual)

    def mudar_rota_aleatoria(self):
        nova_rota = random.choice(self.rotas)
        print(f"\nMudando rota para: {nova_rota}")
        self.rota_atual = nova_rota
        self.notificar_observadores()



# Execução principal

if __name__ == "__main__":
    fabrica = CaminhaoFactory()
    torre = TorreComunicacao()

    # Criando caminhões via fábrica
    caminhao1 = CaminhaoObserver(fabrica.criar_caminhao("comum"), torre)
    caminhao2 = CaminhaoObserver(fabrica.criar_caminhao("reciclavel"), torre)
    caminhao3 = CaminhaoObserver(fabrica.criar_caminhao("hospitalar"), torre)

    rota = RotaLixo(torre)
    rota.adicionar_observador(caminhao1)
    rota.adicionar_observador(caminhao2)
    rota.adicionar_observador(caminhao3)

    print("Sistema de coleta iniciado.\n")

    # Simulação de 3 ciclos com alertas
    for i in range(3):
        print(f"\n========== CICLO {i + 1} ==========")
        alerta = torre.enviar_alerta()
        rota.mudar_rota_aleatoria()
        time.sleep(1.5)

    # Relatório final
    print("\n==============================")
    print("Relatório Automático Final")
    print("==============================")

    for obs in rota.observadores:
        c = obs.caminhao
        print(f"{c.tipo}: {c.coletas} coletas realizadas (Prioridade {c.prioridade})")

    print(f"\nTotal de alertas enviados: {torre.alertas_enviados}")
    print(f"Total de mensagens da torre: {len(torre.historico)}")
