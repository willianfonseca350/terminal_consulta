import ctypes
import time
from rich import print

DWORD = ctypes.c_uint32
char = ctypes.create_string_buffer(16)

# Load the DLL
dll = ctypes.CDLL('.\dll\sc501ger.dll')

result = dll.vInitialize()
result = dll.tc_startserver_port(6501)


class TermTable(ctypes.Structure):
    _fields_ = [    
        ("termName", ctypes.c_char * 256 * 34),
        ("termSock", ctypes.c_int * 256),
        ("termIP", ctypes.c_uint32 * 256),
        ("termTipo", ctypes.c_int * 256),
        ("term_connections", ctypes.c_int),
    ]

# Load the C DLL
dll = ctypes.CDLL("./dll/sc501ger.dll")  # Replace "your_dll_name.dll" with the actual DLL name

# Define the argument and return types for GetTermConectados
dll.GetTermConectados.argtypes = [ctypes.c_int, ctypes.POINTER(TermTable)]
dll.GetTermConectados.restype = ctypes.POINTER(TermTable)

# Create an instance of TermTable
termTable = ctypes.pointer(TermTable())

# # Call the C function
for _ in range(5):
    dll.GetTermConectados(1, termTable)
    result = termTable.contents
    print(result.term_connections)
    if result.term_connections > 0: break
    time.sleep(2)

# # Get the result from the structure

# print(termTable) 
socket_id = 0
for i in range(result.term_connections):
    print("Terminal:", result.termName[i].value.decode("utf-8"))
    print("Socket ID:", result.termSock[i])
    ip = result.termIP[i]
    ip_address = "%d.%d.%d.%d" % (ip & 0xFF, (ip >> 8) & 0xFF, (ip >> 16) & 0xFF, (ip >> 24) & 0xFF)
    print("IP Address:", ip_address)
    # print("IP Address:", result.tabIP[i])
    print("Tipo:", result.termTipo[i])
    print("---")
    socket_id = result.termSock[i]

# print(dll.bEnviaVivo(socket_id))
# print(dll.bSendAllwaysLive(socket_id))
dll.bSendAllwaysLive(socket_id)

# Define the C function prototype with the correct argument types and return type
bReceiveBarcode = dll.bReceiveBarcode
bReceiveBarcode.argtypes = [
    ctypes.POINTER(ctypes.c_int),  # id
    ctypes.POINTER(ctypes.c_int),  # Porta
    ctypes.c_char_p,               # buffer
    ctypes.POINTER(ctypes.c_int)   # Nbr
]
bReceiveBarcode.restype = ctypes.c_bool

def receive_barcode():
    # Create variables to store the result
    id_value = ctypes.c_int()
    porta_value = ctypes.c_int()
    buffer_size = 3500
    buffer_value = ctypes.create_string_buffer(buffer_size)
    nbr_value = ctypes.c_int()

    # Call the C function with the variables as arguments
    result = bReceiveBarcode(ctypes.byref(id_value), ctypes.byref(porta_value), buffer_value, ctypes.byref(nbr_value))

    if result:
        # If the function call is successful, print the barcode data
        print("ID:", id_value.value)
        print("Porta:", porta_value.value)
        print("Buffer:", buffer_value.value[:nbr_value.value].decode('utf-8'))  # Convert to string and remove unused bytes
        print("Nbr:", nbr_value.value)

        bSendProdPrice = dll.bSendProdPrice
        bSendProdPrice.argtypes = [
            ctypes.c_int,        # id
            ctypes.c_char_p,     # NameProd
            ctypes.c_char_p      # PriceProd
        ]
        bSendProdPrice.restype = ctypes.c_bool
        name_c = ctypes.c_char_p('TIJOLÃO 6 FUROS DESCRICAO'.encode('latin-1'))
        price_c = ctypes.c_char_p('1.235,55'.encode('utf-8'))

        # Call the C function with the converted arguments
        result = bSendProdPrice(id_value, name_c, price_c)

        if result:
            print("Product name and price sent successfully.")
        else:
            print("Failed to send product name and price.")
    # else:
    #     print("Failed to receive barcode data.")


print('Listening...')
while True:
    receive_barcode()
    time.sleep(0.1)
dll.vFinalize()
# print(dll.dll_version())
# Print the result
