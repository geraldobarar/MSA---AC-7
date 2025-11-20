from maspy import *
from maspy.learning import *
import datetime  # Necessário para cumprir o requisito da data na entrega

# Constantes para facilitar a leitura e manutenção
SHELF = 0
C1 = 1
C2 = 2
C3 = 3

class AlocadorEnv(Environment):
    def __init__(self, env_name):
        super().__init__(env_name)
        
        # ESTADOS: 16 estados possíveis
        # (4 posições possíveis p/ Obj1 * 4 posições possíveis p/ Obj2)
        # Fórmula: estado = (pos_obj1 * 4) + pos_obj2
        self.create(Percept("objetos_pos", range(16), listed))
        
        # Estado inicial: Ambos na prateleira (0 e 0 -> Estado 0)
        self.possible_starts = {"objetos_pos": [0]} 

    # Lógica de Transição e Recompensas (O "Cérebro" do Ambiente)
    def alocar_transition(self, state_dict: dict, action: int):
        state_int = state_dict['objetos_pos']
        
        # Decodifica o estado atual (matemática inversa da criação dos estados)
        pos_obj1 = state_int // 4
        pos_obj2 = state_int % 4
        
        reward = 0
        terminated = False
        
        # AÇÕES (Mapeamento):
        # 0: Mover Obj1 -> C1 (+5)
        # 1: Mover Obj1 -> C2 (-5)
        # 2: Mover Obj1 -> C3 (+7)  <-- MELHOR PARA OBJ 1
        # 3: Mover Obj2 -> C1 (-5)
        # 4: Mover Obj2 -> C2 (+5)  <-- MELHOR PARA OBJ 2
        # 5: Mover Obj2 -> C3 (-2)
        
        # Lógica de Movimento do Objeto 1 (Ações 0, 1, 2)
        if action in [0, 1, 2]: 
            if pos_obj1 != SHELF: 
                # Punição alta se tentar mover o que já saiu da prateleira para evitar loops
                return state_dict, -20, False 
            
            if action == 0:   
                pos_obj1 = C1
                reward = 5    # [cite: 14]
            elif action == 1: 
                pos_obj1 = C2
                reward = -5   # [cite: 15]
            elif action == 2: 
                pos_obj1 = C3
                reward = 7    # [cite: 16, 17]

        # Lógica de Movimento do Objeto 2 (Ações 3, 4, 5)
        elif action in [3, 4, 5]: 
            if pos_obj2 != SHELF: 
                return state_dict, -20, False
                
            if action == 3:   
                pos_obj2 = C1
                reward = -5   # [cite: 18]
            elif action == 4: 
                pos_obj2 = C2
                reward = 5    # [cite: 19, 20]
            elif action == 5: 
                pos_obj2 = C3
                reward = -2   # [cite: 21]
        
        # Codifica o novo estado
        new_state_int = pos_obj1 * 4 + pos_obj2
        new_state_dict = {'objetos_pos': new_state_int}

        # Condição de Parada: Ambos os objetos saíram da prateleira
        if pos_obj1 != SHELF and pos_obj2 != SHELF:
            terminated = True
        
        return new_state_dict, reward, terminated

    # AÇÃO EFETIVA (Execução no ambiente)
    @action(listed, range(6), alocar_transition)
    def alocar(self, agt, action_code: int):
        percept_result = self.get(Percept("objetos_pos", Any))
        
        current_pos_perc = None

        # Tratamento seguro para extrair o objeto Percept de dentro da lista (se for lista)
        if isinstance(percept_result, list):
            if len(percept_result) > 0:
                current_pos_perc = percept_result[0]
        else:
            current_pos_perc = percept_result

        # --- CORREÇÃO DO ERRO DO PYLANCE (Guard Clause & Assert) ---
        # 1. Se por algum motivo a percepção for None, encerra antes de dar erro.
        if current_pos_perc is None:
            self.print(f"{agt}: Erro crítico - Percepção não encontrada.")
            return

        # 2. Força o sistema de tipos a entender que aqui TEMOS um objeto Percept válido.
        assert isinstance(current_pos_perc, Percept)
        # -----------------------------------------------------------

        current_val = current_pos_perc.values
        
        # Simula a transição para pegar o reward calculado na lógica e imprimir no log
        new_state_dict, reward, _ = self.alocar_transition(
            {'objetos_pos': current_val}, action_code
        )
        new_val = new_state_dict['objetos_pos']
        
        # Configuração de Strings para o log ficar legível na entrega
        locs = {0: "Prat.", 1: "CX 1", 2: "CX 2", 3: "CX 3"}
        act_str = ""
        if action_code < 3: 
            act_str = f"Mover Objeto 1 -> {locs[action_code+1]}"
        else: 
            act_str = f"Mover Objeto 2 -> {locs[action_code-2]}"

        # Verifica se houve mudança de estado e aplica
        if new_val != current_val:
            self.change(current_pos_perc, new_val)
            # Log detalhado para comprovar funcionamento
            is_optimal = "SIM" if reward >= 5 else "NÃO"
            self.print(f"{agt}: {act_str} | Recompensa: {reward} | (Decisão Ótima? {is_optimal})")
        else:
            self.print(f"{agt}: Movimento Inválido ou Repetido ({act_str}) | Recompensa: {reward}")

class AlocadorAgent(Agent):
    def __init__(self, name=None):
        super().__init__(name)
        # O agente usará o modelo treinado, sem necessidade de planos manuais

if __name__ == "__main__":
    # --- COMPROVAÇÃO DE DATA E HORA (Requisito Obrigatório do PDF) ---
    print("\n" + "="*60)
    print(f"DATA E HORA DA EXECUÇÃO: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("ALUNO: Geraldo e Romário") 
    print("="*60 + "\n")

    # --- FASE 1: TREINAMENTO ---
    print(">>> INICIANDO TREINAMENTO (Q-LEARNING)...")
    env_train = AlocadorEnv("AmbienteTreino")
    model = EnvModel(env_train)
    
    # AUMENTADO PARA 15.000 EPISÓDIOS
    # Garante a convergência para as recompensas máximas (+7 e +5) evitando mínimos locais
    model.learn(qlearning, max_steps=50, num_episodes=15000)
    print(">>> TREINAMENTO CONCLUÍDO.\n")
    
    # Limpa percepções residuais do treinamento
    model.reset_percepts()

    # --- FASE 2: EXECUÇÃO ---
    print(">>> EXECUTANDO O AGENTE TREINADO (Modo Inferência)...")
    
    env_run = AlocadorEnv("AmbienteExecucao")
    ag = AlocadorAgent("Robo_Alocador")
    
    # Carrega a política aprendida
    ag.add_policy(model)
    ag.auto_action = True 
    
    # Inicia o sistema
    Admin().connect_to([ag], env_run) 
    Admin().start_system()