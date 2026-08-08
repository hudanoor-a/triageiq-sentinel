# Why does the IP change on stop/start
AWS manages a pool of public IP addresses. Whenver a resource or an instance requires a public IP, AWS hands it over a spare one for the time being the resource is alive. As soon as the instance stops, the IP address becomes available again and AWS may assign it to any other device as required. Thus on every start/stop the IP is change.

# What does the security group enforce
It sits at the network level. Whenever a connection request is made, it validates the facts against the rules, for example, is the request TCP, is it on port 8080, is the source allowed. Only then it allows the handshake to occur. If any of the rule is not fulfilled, the connection is declined and thus it acts as the gatekeeper of the instance.

# What is the request life-cycle for the browser hitting code server
1. My machine sends a connection request to the IP directly, e.g. https://42.203.15.123:8080
2. The SYN request is sent to the IP address which as a data packet travels over the internet to the AWS.
3. AWS routes it to the instance to whom the IP belongs to currently
4. Security group of the IP cross check the request:
	- is it a tcp -> yes
	- is it on port 8080 -> yes
	- is it from the correct source -> yes
	- allows the packet through
5. Code server receives the connection on port 8080 and sends back ACK SYN
6. My browser sends TCP ACK, connection established
7. Browser sends HTTP GET request:
   GET / HTTP/1.1
   Host: 42.203.15.123:8080
8. Code server responds with HTTP 302 redirect (go to the page /login)
9. Browser follows the redirect and logs in using credentials
