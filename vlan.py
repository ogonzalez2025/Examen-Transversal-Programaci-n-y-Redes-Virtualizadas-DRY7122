# vlan normal o extendida

vlan = int(input("Ingresa numero de VLAN: "))

if 1 <= vlan <= 1005:
    print("VLAN de rango normal")
elif 1006 <= vlan <= 4095:
    print("VLAN de rango extendido")
else:
    print("VLAN no valida.")