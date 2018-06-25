import requests
import numpy
debug= True

if (debug):
    import configdebug as conf
else:
    import config as conf



headers= {
    'Authorization':'Bearer '+conf.digital_ocean['token']
    }


response = requests.get('https://api.digitalocean.com/v2/images?per_page=999', headers=headers)
imageLibrary = response.json()['images']

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
    distroFilter= distros[distroIndex-1]
    filteredLibrary = [x for x in imageLibrary if x['distribution'] == distroFilter]

    displayLibrary(filteredLibrary)


def displayLibrary(library):
    for image in library:
        print("name: "+str(image['name']))
        print("id: "+str(image['id']))
        print("slug: "+str(image['slug']))
        print("dist: "+str(image['distribution']))
        print("regions: ")
        regions = image['regions']

        for region in regions:
            print("\t"+region)
        print("min_disk_size: "+str(image['min_disk_size']))

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")

searchWizard(imageLibrary)
