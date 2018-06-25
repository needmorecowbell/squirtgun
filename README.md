# Squirtgun

<p align="center">
    <img src="res/squirtgun.png"></img>
    <br>
    <b>A Digital Ocean Droplet Launcher</b>
</p>


### Requirements

- Digital Ocean API token
- Python 3+

### Installation
 
 1. **Create Key**
  
      `cd keys/ && ssh-keygen`
    
   ```
   Enter file in which to save the key (/root/.ssh/id_rsa): digitaloceanKey
   Enter passphrase (empty for no passphrase): 
   Enter same passphrase again: 
   Your identification has been saved in digitalOceanKey.
   Your public key has been saved in digitalOceanKey.pub.
   ``` 

 2. **Fill in Config** 
      
    Add your Digital Ocean token to config.py using a text editor and update if needed.
  	- [How to Get Access Token](https://www.digitalocean.com/community/tutorials/how-to-use-the-digitalocean-api-v2)
       
 3. **Install requirements** 

     `pip install -r requirements.txt`
 
 4. **Run The Launcher**
        
     `python3 squirtgun.py`

 5. **Connect to Server**

     `ssh -i keys/digitaloceanKey <user>@<master-ip>`

        

