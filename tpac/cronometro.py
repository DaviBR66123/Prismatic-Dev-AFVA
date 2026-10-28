import time

def contagem_regressiva(minutos, mensagem):
    segundos = minutos * 60
    while segundos > 0:
        m, s = divmod(segundos, 60)
        print(f"{mensagem}: {m:02d}:{s:02d}", end="\r")
        time.sleep(1)
        segundos -= 1
    print(f"{mensagem} finalizado!{' ' * 20}")

def pomodoro_timer():
    print("Bem-vindo ao Metodo Pomodoro!")
    print("O método pomodoro é um sistema de estudo onde o usuário usa um intervalo de estudar e descansar, ideal para estudos longos.")
    
    # Usuário definira os tempos
    work_minutes = int(input("Digite o tempo de estudo (em minutos): "))
    break_minutes = int(input("Digite o tempo de descanso (em minutos): "))
    cycles = int(input("Digite quantos ciclos deseja fazer: "))

    for cycle in range(1, cycles + 1):
        print(f"\n Ciclo {cycle} iniciado!")
        contagem_regressiva(work_minutes, "Tempo de estudo")
        contagem_regressiva(break_minutes, "Tempo de descanso")

    print("\n Pomodoro finalizado! Bom trabalho!")

if __name__ == "__main__":
    pomodoro_timer()
