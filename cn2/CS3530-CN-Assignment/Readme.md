main_server.py and main_client.py are in code_main folder
multicast.py in multicast folder
other folders contain seperate file of functions

code_main folder:
To start server:

i) echo mode
python3 main_server.py -e -4/6 port

ii) file transfer mode
python3 main_server.py -f -4/6 port

an extra string "recv" added to file to know the file transfered

iii) ssl echo message mode 
python3 main_server.py -ssl -4/6 port

iv) ssl echo to a specific ip address listen
python3 main_server.py -ssl -4/6 port

v)char server receive message and then send them
python3 main_server.py -chat -4/6 ip port 

-4/6 for corresponding ipv protocol ipv4 or ipv6\

For client mode:

i) echo single message mode
python3 main_client.py -e -s -4/6 ip port

ii)echo loop message mode
python3 main_client.py -e -l -4/6 ip port

iii)echo ssl connection message mode
python3 main_client.py -e -ssl -4/6 ip port

iv)file transfer mode
python3 main_client.py -f filename -4/6 ip port

v)getaddrinfo from client side
python3 main_client.py -i hostname port

vi)chat mode from client side
python3 main_client.py -chat -4/6 ip port

Time stamp for echo message exists

Multicast

i) sender mode 

python3 multicast.py -s -4/6

ii) listner mode

python3 multicast.py -r -4/6

here sender sends a message which is sent to the group correspondingly


chat_program folder:
Contains files for chat program

i) server side program
python3 chat_server.py

ii)client side program
python3 chat_client.py ip port

echo folder contains:
i) start the echoserver
python3 echo_server.py -4/6 port 

ii)client side echo
python3 echo_client.py host port

iii)client side loop message
python3 echo_loop_client.py host port

file_handling folder:

i) server side for receiving file
python3 file_server.py -4/6 port

ii) client side file transfer:
python3 file_cleint.py filename host port

info folder contains:
i)getaddrinfo file
python3 getaddrinfo.py hostname port

multicast folder contains:

i) there are sender and receiver modes for both ipv6 and ipv4 as well

python3 multicast.py -s/-r -4/-6 
which connects to a group ip to either send or receive data
loop for sender, all the receiver listening to that ip receive the sent messages or data

ssl folder contains:
1)client.key,client.pem,server.key,server.pem certificates necessary for connections

2) to start the server file:
python3 ssl_server.py -4/6 port

3) to start the client file :
python3 ssl_client.py host port

folder Q3 contains general socket creation without ecplicit mentioning of ipv or ipv6 using threads

i)for starting server 
python3 12345

ii)for running the client and send the echo and receive it
python3 client_gen.py host port

