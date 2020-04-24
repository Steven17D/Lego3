# Lego3 Example
As Lego3 has a different usage then the old Lego version, we wanted to have a 
basic example. Newcomers should look at this example and hopefully understand better the new 
features of Lego3.
The theme of this example is **the Zoo.**

## Components
### Giraffe
Giraffe is a very important component. Everybody could see the Giraffe because of it's long neck,
therefore we don't want leave on it any unwanted logs.

### Zebra
Zebra isn't as important as a Giraffe, and most people don't even visit it when they go the zoo.
Therefore we don't care if we leave there any logs.
But, we have an easy access to a Zebra and from there we can send information to other 
animals at the Zoo.

__Note:__ It's important to mention that both of this components supports 
SSH, and has python installed on them, as they are pretty regular animals.

## Tools

### Tetanus
Tetanus is the tool we developed for a Giraffe. Tetanus is a simple tool, it listens on a specific
port for UDP packets. Then it sends back the received data to the animal who sent the packet.

## Setup
In our setup we have one Giraffe, whose name is "bob".
We also have 2 Zebras, one name "alice" and the other named "logan".
You could look at their configuration in [pytest.ini](/example/pytest.ini) (pytest configuration file).

