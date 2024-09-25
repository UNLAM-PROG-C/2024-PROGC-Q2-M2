import threading
import random
import time
import sys

ARG_CANT_CLIENTES = 1
CAPACIDAD_GONDOLA = 10
CANT_REPOSITORES = 2
TIEMPO_REPOSICION = 1
TIEMPO_TOMA_PRODUCTO = 1

productos_en_gondola = CAPACIDAD_GONDOLA
turno_repositor = 1
fin_supermercado = False

mutex_gondola = threading.Lock()
cond_gondola = threading.Condition(mutex_gondola)

def reponer_productos(nro_repositor):
  global productos_en_gondola, turno_repositor, fin_supermercado

  while True:
    with cond_gondola:
      while (productos_en_gondola > 0 or turno_repositor != nro_repositor) and not fin_supermercado:
        cond_gondola.wait()
      if fin_supermercado:
        break
      print(f"Repositor {nro_repositor} va a reponer la góndola")
      time.sleep(TIEMPO_REPOSICION)
      productos_en_gondola = CAPACIDAD_GONDOLA
      print("La góndola ha sido rellenada completamente.")
      turno_repositor = (turno_repositor % CANT_REPOSITORES) + 1 
      cond_gondola.notify_all()

def comprar(nro_cliente):
  global productos_en_gondola

  print(f"Cliente {nro_cliente} ha ingresado a comprar.")
  productos_a_tomar = random.randint(1, 2)
  productos_tomados = 0

  while productos_tomados < productos_a_tomar:
    with cond_gondola:
      while productos_en_gondola == 0:
        print(f"Cliente {nro_cliente} detecta la góndola vacía y espera.")
        cond_gondola.notify_all()
        cond_gondola.wait()
      productos_en_gondola -= 1
      print(f"Cliente {nro_cliente} tomó un producto. Productos restantes: {productos_en_gondola}")
    productos_tomados += 1
    time.sleep(TIEMPO_TOMA_PRODUCTO)

  print(f"Cliente {nro_cliente} ha terminado su compra y se va.")

def supermercado(cantidad_de_clientes):
  global fin_supermercado

  hilo_repositor1 = threading.Thread(target=reponer_productos, args=(1,))
  hilo_repositor2 = threading.Thread(target=reponer_productos, args=(2,))
  hilo_repositor1.start()
  hilo_repositor2.start()

  hilos_clientes = [threading.Thread(target=comprar, args=(i,)) for i in range(1, cantidad_de_clientes + 1)]
  for h in hilos_clientes:
    h.start()

  for h in hilos_clientes:
    h.join()

  global fin_supermercado
  fin_supermercado = True
  with cond_gondola:
    cond_gondola.notify_all()

  hilo_repositor1.join()
  hilo_repositor2.join()
  print("Fin de la compra")

if __name__ == "__main__":
  cantidad_de_clientes = int(sys.argv[ARG_CANT_CLIENTES])
  supermercado(cantidad_de_clientes)