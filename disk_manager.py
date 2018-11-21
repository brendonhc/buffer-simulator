"""
Testes do disk_manager

>>> disk = Disk('train-images.idx3-ubyte', 60000)

>>> disk.storage[0].id
0

>>> disk.get(0)
<disk_manager.Page object>

>>> disk.get(59999)
"""

import struct
import array
import numpy as np

path = 'Images/'

class Page:
    def __init__(self, id, data):
        self.id = id
        self.data = data

"""
    class Disk
    
    Essa classe simula o comportamento de um disco de armazenamento do 
    computador inicializado com um arquivo (de imagens exepcionalmente no 
    formato idx) e seu tamanho máximo (número de páginas, no caso, de imagens)
    
    @author Brendon Hudson
"""
class Disk:
    'Inicializa o disco a partir de um arquivo de imagens .idx'
    def __init__(self, filename, size):
        self.size = size
        self.filename = filename
        self.storage = [None] * self.size

        pages = parse_idx(open(path + self.filename, 'rb'))

        for id in range(self.size):
            self.storage[id] = Page(id, pages[id])

    'Obtem a pagina referente ao page_id'
    def get(self, page_id):
        if page_id in range(0, self.size):
            return self.storage[page_id];
        else:
            return None


# parse_idx:
# Função compartilhada entre os grupos que implementaram os Buffers
# para comparação com os mesmos arquivos.
#
# Interpreta um documento no formato IDX (formato das imagens do mnist)
#
# Retorno:
#   - Um array com uma imagem do arquivo 'fd' em cada posição, imagens essas
#  que serão usadas como páginas no disco e no buffer.
def parse_idx(fd):
    DATA_TYPES = {0x08: 'B',  # unsigned byte
                  0x09: 'b',  # signed byte
                  0x0b: 'h',  # short (2 bytes)
                  0x0c: 'i',  # int (4 bytes)
                  0x0d: 'f',  # float (4 bytes)
                  0x0e: 'd'}  # double (8 bytes)

    header = fd.read(4)

    _, data_type, num_dimensions = struct.unpack('>HBB', header)
    data_type = DATA_TYPES[data_type]
    dimension_sizes = struct.unpack('>' + 'I' * num_dimensions,
                                    fd.read(4 * num_dimensions))

    data = array.array(data_type, fd.read())
    data.byteswap()

    if (len(dimension_sizes) == 3):
        return np.array(data).reshape(
            (dimension_sizes[0], dimension_sizes[1] * dimension_sizes[2]))
    else:
        return np.array(data).reshape(dimension_sizes)
