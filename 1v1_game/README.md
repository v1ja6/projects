_**What is this project about?**_

I wanted to make a project where I am able to integrate math together with my code - something which I have not done. Hence, I decided to make a turn-based game project that has three different options:

  1.	Attack – Deals damage to the opponent to lower their health
  2.	Heal – Restores a portion of the player’s own health
  3.	Train – Permanently levels up the player’s Attack or Heal skills for the remainder of the game, hence increasing the           effectiveness of each option
     
The defining feature of this project is that it relies on probability sequences rather than uniform randomness, hence making the game more interesting. For example, a level 1 attack does not randomly pick any number from 0 to 5. It instead employs a weighted distribution where certain damages (i.e. middle numbers) are more favoured than other extreme outcomes such as 0 or 5. 

This writeup will cover the mathematics behind the game. Additionally, this will also cover the logic behind the code and how I used the module “Textual ” to further enhance the user experience of the game.


_**What is the mathematics behind this game?**_

This section details the mathematical framework behind the game’s mechanics. When creating the game a key question arose: How to create the game whereby the damage and heal output (d and h) is dependent on the skill level of the player (s) and also ensures turn-order neutrality.

To address this question, the analysis is broken down into three parts:

  Part I --> Derivation of the probability function that governs damage and healing outputs.
  
  Part II --> The probability function that determines the success rate of player training at each level 
  
  Part III --> The mechanisms used to maintain turn-order neutrality
  
**Part I: Derivation of the probability function**

