### INSTALLATION:
1. git clone https://github.com/DenMaslov/dz6.git
2. cd dz6
3. pipenv shell
4. pipenv install
5. cd app
6. python posts.py


### requires:
 1. redis 
 2. werkzeug 
 3. awesome-slugify
 4. jinja2
 
### TESTED WITH:
* Windows 10
* python 3.9

### Screenshots
![image](https://user-images.githubusercontent.com/76794599/124370688-0bb26800-dc83-11eb-9500-223f5188c165.png)
![image](https://user-images.githubusercontent.com/76794599/124370682-f9d0c500-dc82-11eb-8b45-f6965d1a2ee1.png)
![image](https://user-images.githubusercontent.com/76794599/124370671-ea517c00-dc82-11eb-969c-0cfb258a1f88.png)



### ERRORS
If you get an error: "redis.exceptions.ConnectionError: Error 10061 connecting to localhost:6379." You should install redis and check if it works via "ping" utility.



