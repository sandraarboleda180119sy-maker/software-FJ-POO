import logging
from abc import ABC, abstractmethod
from datetime import datetime

# 1. CONFIGURACIÓN DE LOGS Y EXCEPCIONES
logging.basicConfig(
    filename='errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class DatoInvalidoError(SoftwareFJError):
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    pass

# 2. CLASES BASE (DEBEN IR PRIMERO)
class EntidadBase(ABC):
    """Clase abstracta principal."""
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        return self._id_entidad

class Servicio(EntidadBase):
    def __init__(self, id_servicio, nombre, costo_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def mostrar_detalle(self):
        pass

# 3. CLASES DERIVADAS
class Cliente(EntidadBase):
    def __init__(self, cedula, nombre, email):
        super().__init__(cedula)
        if not str(cedula).isdigit():
            raise DatoInvalidoError(f"La cédula {cedula} debe ser numérica.")
        self.__nombre = nombre 
        self.__email = email

    def __str__(self):
        return f"Cliente: {self.__nombre} (ID: {self.id_entidad})"

class ReservaSala(Servicio):
    def calcular_costo(self, horas=1, descuento=0):
        return max((self.costo_base * horas) - descuento, 0)

    def mostrar_detalle(self):
        return f"Servicio: Sala - {self.nombre}"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1, seguro=True):
        costo = self.costo_base * dias
        return costo * 1.10 if seguro else costo

    def mostrar_detalle(self):
        return f"Servicio: Equipo - {self.nombre}"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas=1, es_remoto=False):
        costo = self.costo_base * horas
        return costo if es_remoto else costo + 50
    
    def mostrar_detalle(self):
        return f"Servicio: Asesoría - {self.nombre}"

# 4. GESTIÓN DE RESERVAS
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, cantidad):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"

    def procesar(self):
        try:
            if self.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")
            costo = self.servicio.calcular_costo(self.cantidad)
            self.estado = "Confirmada"
            print(f"✓ Reserva {self.id_reserva} exitosa. Costo: ${costo}")
            logging.info(f"Reserva {self.id_reserva} procesada correctamente.")
        except Exception as e:
            raise ServicioNoDisponibleError(f"Fallo en reserva {self.id_reserva}") from e

# 5. SISTEMA Y SIMULACIÓN (LAS 10 OPERACIONES)
class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []

    def ejecutar(self, nombre_op, tarea):
        print(f"\n>>> Op: {nombre_op}")
        try:
            tarea()
            print("Resultado: OK")
        except Exception as e:
            print(f"Resultado: ERROR CONTROLADO -> {e}")
            logging.error(f"Error en {nombre_op}: {e}")

    def iniciar(self):
        # 1. Cliente válido
        self.ejecutar("Reg. Cliente 1", lambda: self.clientes.append(Cliente("123", "Juan", "j@m.com")))
        # 2. Cliente inválido (Letras en ID)
        self.ejecutar("Reg. Cliente 2", lambda: self.clientes.append(Cliente("ABC", "Error", "e@m.com")))
        
        sala = ReservaSala("S1", "Sala A", 100)
        pc = AlquilerEquipo("E1", "Laptop", 50)
        
        # 3. Reserva válida sala
        self.ejecutar("Reserva Sala OK", lambda: Reserva(1, self.clientes[0], sala, 2).procesar())
        # 4. Reserva inválida (Cantidad negativa)
        self.ejecutar("Reserva Error Cantidad", lambda: Reserva(2, self.clientes[0], sala, -5).procesar())
        # 5. Cálculo Alquiler con Seguro
        self.ejecutar("Costo Equipo", lambda: print(f"Total: {pc.calcular_costo(3, True)}"))
        # 6. Registro Cliente 3
        self.ejecutar("Reg. Cliente 3", lambda: self.clientes.append(Cliente("456", "Marta", "m@m.com")))
        # 7. Reserva Equipo OK
        self.ejecutar("Reserva Equipo OK", lambda: Reserva(3, self.clientes[-1], pc, 1).procesar())
        # 8. Intento de acceso a dato privado (Encapsulación)
        self.ejecutar("Prueba Encapsulación", lambda: print(self.clientes[0].__nombre))
        # 9. Asesoría Presencial
        ase = AsesoriaEspecializada("A1", "Java", 80)
        self.ejecutar("Asesoría Presencial", lambda: print(f"Costo: {ase.calcular_costo(2, False)}"))
        # 10. Verificación final
        self.ejecutar("Estado Final", lambda: print(f"Clientes en sistema: {len(self.clientes)}"))

if __name__ == "__main__":
    app = SistemaSoftwareFJ()
    app.iniciar()
