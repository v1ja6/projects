_**What is this project about?**_

I wanted to make a project where I am able to integrate math together with my code - something which I have not done. Hence, I decided to make a turn-based game project that has three different options:

  1.	Attack – Deals damage to the opponent to lower their health
  2.	Heal – Restores a portion of the player’s own health
  
The defining feature of this project is that it relies on probability sequences rather than uniform randomness, hence making the game more interesting. For example, a level 1 attack does not randomly pick any number from 0 to 5. It instead employs a weighted distribution where certain damages (i.e. middle numbers) are more favored than other extreme outcomes such as 0 or 5. 

There is a pdf document that covers the mathematics behind the game in this repository.

To run the game, open up terminal and run "python 1v1_game.py".



_**Brief description of the code behind the game**_

This game uses textualize as the user-interface. 
For the probabilities, I decided to hard code them as there is only a limited number of probabilities that can occur.
In the textualize class, I used an if-elif statement to rotate between player 1 and 2 using the "self.turn" variable.
The code also allows for the player to click or use the keyboard in order to input the options. 
Additionally, the CSS folder helps to further modify the user-interface

This is just a small overview of the code that was used.
