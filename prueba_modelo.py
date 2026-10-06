from models import Cliente

ana = Cliente(1, "  ana  ", "pérez", "ANA@Ejemplo.com", "0987654321", "guayaquil", "Av. 1")

print(ana.nombre)            # 'Ana'              -> el setter limpió y capitalizó
print(ana.email)             # 'ana@ejemplo.com'  -> en minúsculas
print(ana.nombre_completo)   # 'Ana Pérez'        -> propiedad calculada, sin paréntesis
print(ana.dominio_email)     # 'ejemplo.com'
print(Cliente.total_creados) # 1                  -> atributo de clase

ana.ciudad = "quito"         # pasa por el setter
print(ana.ciudad)            # 'Quito'

# ana.id = 99                -> AttributeError: property has no setter
# ana.email = "roto"         -> ValueError: Email inválido: 'roto'
# print(ana.__nombre)        -> AttributeError: es privado
print(ana._Cliente__nombre)  # 'Ana'  <- así lo renombra Python por dentro