# Setting Up File Server through Django
#### Initial Prompt
I am developing a django website that will act as basically the home base of my life, I want to have access to control smart appliances, data logging on different aspects of my personal life. Currently the idea is to put all of this on my rasberry pi 5 with 8gb of ram. I want to know if it would be possible to also integrate file storage and management into the django project. I see people use their Pi's as NAS's that allow them file and media storage. I don't need media storage Is that possible and how hard would it be. Finally could my raspberry pi handle it. Some more information about my use case includes the following: I will only be accessing this server from outside of the network; I will set up port forwarding and use a dynamic DNS to reach my server outside of the network. If possible, in addition to being able to view and add/delete files, I would like to view the physical file and possibly edit the file right from the website if possible. Most of my files will be markdowns used for note-taking, with some photos as well. I don't want to hand-roll my own web-based markdown editor, though, so I would need some sort of open-source plug-and-play option. 

## Table of Contents
1. Overview
2.  
3.  
4.  
5.  
6. 
7. Implementing SMB (Deprecated)

It is definitely possible to integrate file storage and management into your Django project on your Raspberry Pi 5. Here's a breakdown of how to achieve this and the considerations for your use case:

### 1. **File Storage Integration**
   Since you're not dealing with media-heavy files, your Raspberry Pi 5 should be able to handle the storage and access requirements. Given your 8GB of RAM, the Raspberry Pi 5 has sufficient capacity for a lightweight NAS setup, especially for markdown files and some photos.

   **Using Django for File Management:**
   - You can integrate a simple file storage and management system in Django. A common approach is to use **Django's FileField** or **ImageField** for file handling.
   - For viewing and editing markdown files, you can store these files in a designated folder within the project and create views in Django that allow for listing, viewing, and downloading files.

### 2. **Viewing and Editing Files from the Website**
   - For **viewing and editing markdown files**, you could use an open-source markdown editor like **Django-MarkdownX**, which is plug-and-play. This would allow you to edit markdown files directly from the website without writing your own markdown editor.
   - **File uploading and editing**: You can allow users to upload new markdown files and modify them through the website. This could be achieved with a basic Django form for markdown files, integrated with MarkdownX for easy inline editing.

### 3. **NAS Setup on the Raspberry Pi**
   Since you're considering using your Raspberry Pi as a NAS, Samba is an excellent choice for file sharing over the network. You can create a **Samba share** that’s accessible through your Django project and used to store files. 

   To set up:
   - Install and configure Samba on your Pi.
   - In Django, you can set the file storage directory to point to the mounted Samba share.

### 4. **Security Considerations**
   Since you’ll be accessing this from outside your network, consider securing your server with the following:
   - **SSL/TLS encryption**: Use Let's Encrypt or another certificate provider to secure your website.
   - **VPN**: If you want an additional layer of security, setting up a VPN would be helpful for connecting securely to your home network.
   - **Port forwarding and Dynamic DNS**: You’ll need to set up port forwarding on your router, and a service like No-IP or DynDNS can handle dynamic DNS for external access.

### 5. **Performance and Limitations**
   The Raspberry Pi 5 with 8GB of RAM can handle the use case you described. While performance may be impacted if you were dealing with large files or multiple users, for markdown files, photos, and some light smart appliance control, it should be fine. You'll want to ensure that you manage processes efficiently, possibly by using cron jobs or task schedulers for periodic tasks like backups or log collection.

### Suggested Setup:
   - **Django-MarkdownX** for markdown editing.
   - **Samba** for file storage.
   - **Django's FileField** to manage file uploads and browsing.
   - **SSL/TLS** and/or **VPN** for secure access.








## 2. Implementing SMB
For your use case, where you're aiming to set up file storage and management on your Raspberry Pi 5 using Samba (SMB protocol), here's a step-by-step breakdown of the implementation and execution:

### **Overview of SMB and Samba**
- **SMB (Server Message Block)** is a network protocol that allows systems to share files and printers over a network. 
- **Samba** is a free, open-source implementation of SMB/CIFS that enables file and print services on Unix-like systems (like Raspberry Pi with Linux OS).
  
You will use Samba to create network-shared folders that can be accessed from other devices, such as your computer, through the SMB protocol. This is useful in your case for file storage and management, allowing your Django app to access and manage files stored on the Pi.

### **1. Setting up Samba on Raspberry Pi**

#### **Step 1: Install Samba**
First, you’ll need to install Samba on your Raspberry Pi:
```bash
sudo apt update
sudo apt install samba samba-common-bin
```

#### **Step 2: Create a Shared Directory**
You'll need to create a directory on your Pi that you want to share over the network. For example:
```bash
sudo mkdir -p /home/pi/shared
```
This directory will hold the files you plan to manage or serve through your Django app.

#### **Step 3: Configure Samba**
Now you need to configure Samba to share this directory. You’ll edit the Samba configuration file (`/etc/samba/smb.conf`) to include your shared folder.
```bash
sudo nano /etc/samba/smb.conf
```
Add the following at the end of the file:
```
[Shared]
   path = /home/pi/shared
   available = yes
   valid users = pi
   read only = no
   browsable = yes
   public = yes
   writable = yes
```

Explanation of options:
- **path**: Path to the folder you want to share.
- **valid users**: Specifies which users can access the share (e.g., `pi` is the default user).
- **writable**: Enables writing to the folder.

#### **Step 4: Set Samba User**
Next, you need to create a Samba user to allow access to the shared folder. This can be the same as your Pi user (`pi`):
```bash
sudo smbpasswd -a pi
```
You’ll be prompted to enter a password for this user.

#### **Step 5: Restart Samba Service**
Restart Samba to apply the changes:
```bash
sudo systemctl restart smbd
```

#### **Step 6: Set Folder Permissions**
Ensure that the shared folder has the right permissions for the user `pi` to read/write:
```bash
sudo chown -R pi:pi /home/pi/shared
sudo chmod -R 775 /home/pi/shared
```

### **2. Accessing the Shared Folder from Other Devices**

Once Samba is set up, you should be able to access the shared folder from another computer on the same network.

- On **Windows**, you can open File Explorer and type `\\raspberrypi\Shared` in the address bar, or use the Pi’s IP address like `\\192.168.x.x\Shared`.
- On **Linux or macOS**, you can use the `Connect to Server` feature in your file manager and enter `smb://raspberrypi/Shared`.

### **3. Using Samba in Your Django Project**

#### **Django Integration**
You can now integrate this Samba-shared folder into your Django project. Here's how you might approach it:

- **Access files via Django**: You can mount the SMB share on your Raspberry Pi or access it directly through your Django app.
  - If you're mounting the share, you would do something like this:
    ```bash
    sudo mount -t cifs -o username=pi,password=yourpassword //localhost/Shared /mnt/smb
    ```
    Now, `/mnt/smb` acts as your file system for shared files. You can configure Django to access files directly from this mount point.

- **Django File Management**: In your Django settings, configure the `MEDIA_ROOT` or any custom file storage class to point to the mounted shared directory (`/mnt/smb`):
    ```python
    MEDIA_ROOT = '/mnt/smb/'
    MEDIA_URL = '/media/'
    ```

#### **Automating File Handling**
In Django, you can manage uploaded files or other assets within the shared Samba directory. You could allow users to upload files through the Django interface and store them directly on the Pi’s shared folder, where they are available over the network.

### **4. Additional Considerations for Samba Setup**

- **Security**: Ensure your Samba shares are secured, especially if the network is not private. You can limit access to the shared folder by adding specific users or using authentication.
  
- **Backup and Maintenance**: If you’re storing personal life data, consider setting up regular backups of the shared directory using tools like `rsync` or scheduling them with cron jobs.

- **Mounting on Boot**: To make sure your shared directory is mounted automatically after each reboot, you can add an entry to your `/etc/fstab` file:
    ```
    //localhost/Shared /mnt/smb cifs username=pi,password=yourpassword 0 0
    ```

### **5. Monitoring Samba**
You can monitor the performance and usage of your Samba server by checking the Samba logs located at `/var/log/samba/`. This will help ensure that your Raspberry Pi is handling file sharing smoothly without overloading.

### **Conclusion**
Setting up Samba on your Raspberry Pi for your Django project is relatively straightforward. By creating a network-shared folder, you can integrate it into Django for file management. The Raspberry Pi 5’s improved specs should comfortably handle this use case, especially since you're not dealing with large media files.


