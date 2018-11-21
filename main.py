from disk_manager import Disk
from buffer_manager import Buffer
import random
import threading

N_SEARCHES = 100000  # Fixo
SIZE_DISK_A = 10000
SIZE_DISK_B = 60000
SIZE_BUFFER_A = (1, 2, 10, 100, 500, 1000, 5000, 10000)
SIZE_BUFFER_B = (6, 60, 600, 6000, 60000)
DB_FILE_A = 't10k-images.idx3-ubyte'
DB_FILE_B = 'train-images.idx3-ubyte'


# Classe principal que gerencia a simulação do buffer
class BufferSimulatorThread (threading.Thread):
    def __init__(self, size_buffer, size_disk, n_searches, dbfilename):
        super().__init__()
        self.collisions = 0
        self.n_searches = n_searches
        self.disk = Disk(dbfilename, size_disk)
        self.buffer = Buffer(size_buffer, self.disk)

    def run(self):

        self.collisions = 0

        # Simulação de N_SEARCHES de buscas no buffer contando as colisões:
        for count in range(self.n_searches):
            page_id = random.randrange(self.disk.size)

            if not self.buffer.find(page_id):
                self.collisions += 1
                self.buffer.insert(page_id)


    # Impressão de relatórios
    def print_report_a(self):
        print('Buffer contendo no máximo ' + str(self.buffer.size) + ' ' +
        'imagens ou ' + str(self.buffer.size*100/self.disk.size) + '% da base '
        'de dados, após', self.n_searches,'consultas,',
              str(self.collisions*100/self.n_searches) +
              '% não estavam presentes no buffer.')

    def print_report_b(self):
        print('---------------------------------------------')
        print('Precisão: ', (self.n_searches-self.collisions)/self.n_searches) #
        # acertos/buscas
        print()
        print('Buscas: ', self.n_searches)
        print('Colisões no buffer: ', self.collisions)
        print('Frequência de colisão no buffer: ', self.collisions/self.n_searches)
        print()
        print('Tamanho do buffer: ', self.buffer.size)
        print('Tamanho da database: ', self.disk.size)
        print('Tamanho do buffer / Tamanho da database: ',
              self.buffer.size/self.disk.size)


###################################################################
########## Simulações de buffer e geração de relatórios ###########
###################################################################

# Instanciação dos objetos para:
threads_test1 = []
threads_test2 = []
threads_test3 = []

# Relatórios formatados em frases para 10k e depois 60k de imagens (páginas)
for i in range(8):
    threads_test1.append(BufferSimulatorThread(SIZE_BUFFER_A[i], SIZE_DISK_A,
                                        N_SEARCHES, DB_FILE_A)) # 10k
    threads_test2.append(BufferSimulatorThread(SIZE_BUFFER_A[i], SIZE_DISK_B,
                                               N_SEARCHES, DB_FILE_B))  # 10k

# Relatório em lista para 60k de imagens (páginas) mas com diferentes buffers
for i in range(5):
    threads_test3.append(BufferSimulatorThread(SIZE_BUFFER_B[i], SIZE_DISK_B,
                                               N_SEARCHES, DB_FILE_B)) #60k


# Todas as threads em um array para facilitar
threads = threads_test1 + threads_test2 + threads_test3


# Simulações
for thread in threads:
    thread.start()

# Aguarda a finalização de cada thread e em seguida imprime seu respectivo
# relatório de execução:
print('Relatórios do Buffer - Algoritmo de Paginação FIFO\n\n')
for thread in threads:
    # Indicadores de testes
    if thread == threads_test1[0]:
        print('Base de dados de 10000 imagens\n')
    elif thread == threads_test2[0]:
        print('\n\nBase de dados de 60000 imagens\n')
    elif thread == threads_test3[0]:
        print('\n\n')

    thread.join()

    # Seguindo o padrão de impressão semelhante ao do outro grupo
    # Padrão esse que pode ser modificado sem problemas.
    thread.print_report_a()

print('\n\n\n')
for thread in threads_test3:
    thread.print_report_b()
