Working example set of three apps:

* `main.py` is the paint app that acts as receiver and publisher: it sends the points and color of the drawn line, and also receives line info from the server
* `server.py` implements the forwarder design and broadcasts messages to all subscribers
* **deprecated** `receiver.py` an app with an empty paint widget that cannot handle user input, but draws whatever it receives

Run the server first, then the other two apps, and start drawing :)