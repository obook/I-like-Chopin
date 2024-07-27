#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Fichier : bibliotheque_interfaces.py
# Auteur : OB
# Groupe : NSI
# Date : 08/01/2024
# Version : 1.6
# Dépendance : netifaces2
# Description : Bibliothèque qui liste les adresses IP de la machine avec les adresses MAC
# Utilisation :
# from interfaces_reseau import get_interfaces, get_hostname
# interfaces = get_interfaces()
# Exemple de liste obtenue :
# [{'ip': '192.168.56.1'}, {'ip': '169.254.229.202'}]

import netifaces # compatible avec netifaces2

# Sous fonction de remplissage de la liste des IP
def __add_ip(family_addresses:list, liste:list, local:bool = False) -> bool :
    if not family_addresses:
        return False
    for address in family_addresses :
        ip = address['addr']
        if ip =='0.0.0.0' :
            return False
        if ip=='127.0.0.1' and not local :
            return False
        liste.append( {'ip':ip} )
        return True

# Fonction qui retourne dans une liste de dictionnaires ip/mac de la machine
def get_interfaces(localip:bool = False, IpV6:bool = False) -> list :
    ips_list =[]
    interfaces = netifaces.interfaces()
    for interface in interfaces :
        addresses = netifaces.ifaddresses(interface)
        if IpV6 :
            for address_family in (netifaces.AF_INET, netifaces.AF_INET6) :
                family_addresses = addresses.get(address_family)
                __add_ip(family_addresses, ips_list, localip)
        else :
            family_addresses = addresses.get(netifaces.AF_INET)
            __add_ip(family_addresses, ips_list, localip)
    return ips_list

# Programme principal qui ne s'exécute pas si le script est appelé par un 'import' (comme une bibliothèque)
if __name__ == '__main__' :
    print("Liste des adresses IP de la machine")
    print("***********************************")
    interfaces = get_interfaces(True, False)
    for interface in interfaces :
        print("IP =", interface['ip'])
