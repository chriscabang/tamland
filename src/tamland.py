import socket

# Server IP address and port
server_ip = 'localhost'  # or '127.0.0.1'
server_port = 9980  # Port number to listen on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {server_ip}:{server_port}")

while True:
  try:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    #print(f"Accepted connection from {client_address}")

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print(f"Received data: {client_address} {data}")

    # Process the received data or perform other operations

    # Send a response back to the client
    #response = "Hello, client!"
    #client_socket.sendall(response.encode())

    # Close the client socket
    client_socket.close()
  except KeyboardInterrupt:
    exit(1)
