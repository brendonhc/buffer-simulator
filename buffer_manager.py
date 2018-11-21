'''
Testes do buffer_manager

>>> disk = Disk('train-images.idx3-ubyte', 60000)

>>> buffer = Buffer(10000, disk)

>>> buffer.find(1)
False

>>> buffer.insert(59999)

>>> buffer.find(59999)
True
'''

from disk_manager import Disk
from collections import deque

"""
    class Buffer:
    
    Classe que simula o comportamento de um buffer utilizando as políticas 
    de substituição de páginas do algoritimo FIFO.
    
    @author Brendon Hudson
"""
class Buffer:
    '''Inicializa um objeto Buffer dado um tamanho máximo em número de
    páginas para sua memória e dado um objeto Disk() qual o alimentará com
    páginas'''
    def __init__(self, size, disk):
        self.size = size;
        self.mem = deque(maxlen=self.size)
        self.disk = disk

    'Busca por uma página na memória do buffer dado seu id'
    def find(self, page_id):
        for page in self.mem:
            if page.id == page_id:
                return True

        return False

    'Insere uma página do disco no buffer dado seu id'
    def insert(self, page_id):
        self.mem.append(self.disk.get(page_id))
