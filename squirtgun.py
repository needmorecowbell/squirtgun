import time
import digitalocean
from digitalocean import SSHKey
import paramiko
import os

import requests
import numpy
debug= True

if (debug):
    import configdebug as conf
else:
    import config as conf

def createKey():
    user_ssh_key = open(conf.digital_ocean['ssh-key']).read()
    key = SSHKey(token=conf.digital_ocean['token'],
                 name="template-ssh-key",
                 public_key=user_ssh_key
            )
    try:
        key.create()
    except Exception as e:
        print("[!] Already Created: "+str(e))
        return


    print('[+] Key Added to DigitalOcean Account')


def searchWizard(imageLibrary):
    #Search by Distro
    distroSet = set()
    for distro in imageLibrary:
        distroSet.add(distro['distribution'])

    print("Distributions:\n")
    distros = list(distroSet)
    distroIndex=1
    for distro in distros:
        print("\t"+str(distroIndex)+") "+str(distro))
        distroIndex+=1

    distroIndex = int(input("\nEnter the number of the distro you'd like to search for: "))
    print("")
    distroFilter= distros[distroIndex-1]
    filteredLibrary = [x for x in imageLibrary if x['distribution'] == distroFilter]

    imageIndex=1
    idList=[]
    for image in filteredLibrary:
        print("Image "+str(imageIndex)+": ")
        print("\tname: "+str(image['name']))
        print("\tid: "+str(image['id']))
        print("\tslug: "+str(image['slug']))
        print("\tdist: "+str(image['distribution']))
        idList.append((str(image['id']),image['name']))
        imageIndex+=1
#        print("regions: ")
#        regions = image['regions']

        #for region in regions:
        #    print("\t"+region)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    idChoice = idList[int(input("\nEnter the id of the image you'd like to select: "))-1]

    return idChoice

def getSize():

    sizeResponse = requests.get('https://api.digitalocean.com/v2/sizes', headers=headers)
    sizeLibrary = sizeResponse.json()
    slugSet=[]
    count=1

    for size in sizeLibrary['sizes']:
        print("\nPlan "+str(count)+":")
        print("\tslug: "+str(size['slug']))
        slugSet.append(str(size['slug']))
        print("\tmemory: "+str(size['memory'])+"\tvcpus: "+str(size['vcpus'])+"\tdisk: "+str(size['disk']))
        print("\tEst. Monthly Price: $"+str(size['price_monthly']))
        count+=1

    slugIndex = int(input("Enter Plan number: "))-1

    return slugSet[slugIndex]

if __name__ == '__main__':

    headers= {
        'Authorization':'Bearer '+conf.digital_ocean['token']
        }


    response = requests.get('https://api.digitalocean.com/v2/images?per_page=999', headers=headers)
    imageLibrary = response.json()['images']



    imageid,imageName= searchWizard(imageLibrary)
    print("Selection size plan: ")
    sizeSlug= getSize()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Image id: "+str(imageName)+"\t Size: "+str(sizeSlug))

    print('[-] Adding SSH key to manager')
    createKey()

    print("[-] Creating Droplet ")
    hostname= input("Enter hostname: ")
    region= input("Enter region: ")

    region="nyc1"
    manager = digitalocean.Manager(token=conf.digital_ocean['token'])
    keys= manager.get_all_sshkeys()

    print("[-] Creating Digital Ocean Droplet ["+hostname+","+imageid+"]...")


    droplet = digitalocean.Droplet(token=conf.digital_ocean['token'],
                                   name=hostname,
                                   region=region,
                                   image= imageid,
                                   size_slug= sizeSlug,
                                   backups=False,
                                   ssh_keys=keys
                                   )
    droplet.create()

    print("[+] Droplet Creation initiated")
    print("[-] Checking for status...")

    status=""
    while(status != "completed"): #ping for server creation
        actions= droplet.get_actions()

        for action in actions:
            action.load()
            status=action.status
            print("[-]\t"+ action.status)

        time.sleep(3)

    print("[+] Droplet["+hostname+","+imageName+"] Complete")
    load=droplet.load()
    ip=load.ip_address
    print("[-] Droplet information:")
    print("[-]\tDroplet ID:"+str(droplet.id))
    print("[-]\tIPV4:"+load.ip_address)

    print("[+] Droplet Connection: \n\t ssh -i keys/digitaloceanKey root@"+str(ip))



    if(input("Would you like to destroy droplet? y/n: ") =="y"):
        print("[-] Destroying Droplet...")
        droplet.destroy()
        print("[+] Droplet Destroyed.")

