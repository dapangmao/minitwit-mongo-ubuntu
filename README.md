This is a quick tutorial to deploy a web service (a social network) by the LNMP (Linux, Nginx, MongoDB, Python) infrastructure on any IaaS cloud. The repo at Github is at https://github.com/dapangmao/minitwit-mongo-ubuntu. 

#### Stack
The stack is built on the tools in the ecosystem of Python below. 

| Tool   |      Name      |  Advantage |
|----------|:-------------:|------|
| Cloud | [DigitalOcean](https://www.digitalocean.com/) | Cheap but fast |
| Server distro |  Ubuntu 14.10 x64 | Everything is latest |
| WSGI proxy |    Gunicorn   |   Manage workers automatically |
| Web proxy | Nginx |    Fast and easy to configure|
| Framework | Flask |Single file approach for MVC |
| Data store | MongoDB | No scheme needed and scalable|
| DevOps | Fabric | Agentless and Pythonic  |

In addition, a [Supervisor](http://supervisord.org/) running on the server provides a daemon to protect the Gunicorn-Flask process. 

#### The MiniTwit app
The MiniTwit application is [an example provided by Flask](https://github.com/mitsuhiko/flask/tree/master/examples/minitwit), which is a prototype of Twitter like multiple-user social network. The original application depends on SQLite. However, the data store could be modified to fit the category of NoSQL such as Google Data Store or MongoDB. A live MintiTwit demo is hosted at http://minitwit-123.appspot.com/public

#### Deployment

##### 1. Install Fabric and clone the Github repo
The DevOps tool is [fabric](https://github.com/fabric/fabric) that is simply based on SSH. The `fabfile.py` and the staging `flask` files are stored on Github. We should install `fabric` and download the fabfile.py on the local machine before the deployment.
```bash
sudo pip install fabric 
wget https://raw.githubusercontent.com/dapangmao/minitwit-mongo-ubuntu/master/fabfile.py
fab -l
```

##### 2. Input IP from the virtual machine
A new VM usually emails IP address and the root password. Then we could modify the head part of the `fabfile.py` accordingly. There are quite a few cheaper cloud provider for prototyping other than Amazon EC2. For example, a minimal instance from DigitalOcean only costs five dollars a month. If SSH key has been uploaded, the password could be ignored. 

```python
env.hosts = ['YOUR IP ADDRESS'] # <--------- Enter the IP address
env.user = 'root'
env.password = 'YOUR PASSWORD'  # <--------- Enter the root password
```

##### 3. Fire up Fabric
Now it is time to formally deploy the application. With the command below, the `fabric` will first install `pip, git, nginx, gunicorn, supervisor` and the latest `MongodB`, and configure them sequentially.  In less than 5 minutes, a Flask and MongoDB application will be ready for use. Since DigitalOcean has its own software repository for Ubuntu, and its VMs are on SSD, the deployment is even faster, which is usually finished in one minute.   
```python
fab deploy_minitwit
```


