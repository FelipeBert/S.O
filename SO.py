import threading
import time

banco_de_dados = 0
leitores_ativos = 0
escritores_ativos = 0
leitores_lock = threading.Lock()
escritores_lock = threading.Lock()
leitores_count_lock = threading.Lock()
escritores_count_lock = threading.Lock()

class Leitor(threading.Thread):
    def run(self):
        while True:
            self.ler()
            time.sleep(1)

    def ler(self):

        global banco_de_dados
        with leitores_lock:
            global leitores_ativos
            leitores_ativos += 1

            if leitores_ativos == 1:
                escritores_lock.acquire()

        with leitores_count_lock:
            print(f"Leitores ativos: {leitores_ativos}")
        print(f"Leitor lendo: {banco_de_dados}")

        with leitores_lock:
            leitores_ativos -= 1
            if leitores_ativos == 0:
                escritores_lock.release()
        time.sleep(1)

class Escritor(threading.Thread):

    def run(self):
        while True:
            with escritores_lock:
                self.escrever()
            time.sleep(3)

    def escrever(self):

        global banco_de_dados
        with escritores_count_lock:
            global escritores_ativos
            escritores_ativos += 1

        novo_dado = banco_de_dados + 1
        banco_de_dados = novo_dado

        print(f"Escritores ativos: {escritores_ativos}")
        print(f"Escritor escreveu: {novo_dado} vezes")

        with escritores_count_lock:
            escritores_ativos -= 1

def main():
    num_leitores = 5
    num_escritores = 2

    leitores = [Leitor() for _ in range(num_leitores)]
    escritores = [Escritor() for _ in range(num_escritores)]

    for leitor in leitores:
        leitor.start()

    for escritor in escritores:
        escritor.start()

    for leitor in leitores:
        leitor.join()

    for escritor in escritores:
        escritor.join()

if __name__ == "__main__":
    main()
