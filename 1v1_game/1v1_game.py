import numpy as np
from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Button, ProgressBar, RichLog, Static
from rich.text import Text

#Class that focuses on the health of th player
class Health:
    def __init__(self, health):
        self.health = health

    def health_deductor(self, damage):
        return max(0, self.health - damage)

    def health_adder(self, healing):
        return min(100, self.health + healing)


#Probabilities for attack
def attack_prob(level):
    if level == 0:
        probability = {0: 0.432, 1: 0.253, 2: 0.148, 3: 0.086, 4: 0.051, 5: 0.030}

    if level == 1:
        probability = {0: 0.308, 1: 0.308, 2: 0.180, 3: 0.105, 4: 0.063, 5: 0.036}

    if level == 2:
        probability = {0: 0.207, 1: 0.353, 2: 0.207, 3: 0.121, 4: 0.071, 5: 0.041}

    if level == 3:
        probability = {0: 0.158, 1: 0.269, 2: 0.269, 3: 0.158, 4: 0.092, 5: 0.054}

    if level == 4:
        probability = {0: 0.112, 1: 0.192, 2: 0.327, 3: 0.192, 4: 0.112, 5: 0.065}
   
    array = np.array(list(probability.values()))
    number = np.random.choice(list(probability.keys()), p = array)
    return number

#Probabilities for heal
def heal_prob(damage_dealt):
    if damage_dealt < 3:
        probability = {1: 0.2 , 2: 0.6, 3: 0.2}

    elif damage_dealt == 3:
        probability = {0: 0.1 , 1: 0.6, 2: 0.3}

    elif damage_dealt == 4:
        probability = {0: 0.3 , 1: 0.5, 2: 0.2}

    elif damage_dealt == 5:
        probability = {0: 0.6 , 1: 0.3, 2: 0.1}
   

    array = np.array(list(probability.values()))
    number = np.random.choice(list(probability.keys()), p = array)
    return number

#Function that deals with the level up feauture of attack
def attack_level_prob():
    probability = {0: 0.65, 1: 0.35}
    array = np.array(list(probability.values()))
    number = np.random.choice(list(probability.keys()), p = array)
    return number

# =========================================================

   
class FightingGame(App):
    #Calls the css file
    CSS_PATH = "textual_style.tcss"
    
    #Key binds for the game
    BINDINGS = [("q", "quit", "Quit Game"),
                ("a", "attack", "Attack Player"),
                ("h", "heal", "Heal Player"),
                ]

    #====================
    p1_hp = 15
    p2_hp = 15


    attack_level_p1 = 0
    attack_level_p2 = 0

    cooldown_p1 = 0
    cooldown_p2 = 0

    heal_deductor_p1 = 0
    heal_deductor_p2 = 0

    levelup_p1 = 0
    levelup_p2 = 0               
    #====================
    
    def compose(self):
        
        yield Header()
        
        # Horizontal layout splitting Player 1 and Player 2
        yield Horizontal(
            #===PLAYER 1===
            Vertical(
                Static("[bold cyan]Player 1[/bold cyan]"),
                Horizontal(
                    ProgressBar(id="p1_health", total=15, show_percentage=False, show_eta=False),
                    Static(f" {self.p1_hp}", id="p1_health_text"),
                    id="p1_health_container"  
                ),
                ProgressBar(id="level_bar_p1", total=3, show_percentage=False, show_eta=False),  
                Static(f"[bold cyan]\nAttack Level: {self.attack_level_p1} [/bold cyan]", id = "attack_training_p1"),
                Static(f"[bold cyan]Player is not wounded!", id = "wounded_p1"),    
                Static("[cyan]\nOptions:[/cyan]"),
                
                #Options for player 1
                Horizontal(
                    Button("Attack", id="button_attack_p1")
                ), 
                Horizontal(
                    Button("Heal", id="button_heal_p1"),
                ),
  
                classes="player-box"
            ),
            #===PLAYER 2===
            Vertical(
                Static("[bold red]Player 2[/bold red]"),
                Horizontal(
                    ProgressBar(id="p2_health", total=15, show_percentage=False, show_eta=False),
                    Static(f" {self.p2_hp}", id="p2_health_text"),
                    id="p1_health_container"
                ),
                ProgressBar(id="level_bar_p2", total=3,  show_percentage=False, show_eta=False),
                Static(f"[bold red]\nAttack Level: {self.attack_level_p2} [/bold red]", id = "attack_training_p2"),
                Static(f"[bold red]Player is not wounded!", id = "wounded_p2"),
                Static("[red]\nOptions:[/red]"),

                #Options for player 2
                Horizontal(
                    Button("Attack", id="button_attack_p2"),
                ),
                Horizontal(
                    Button("Heal", id="button_heal_p2"),
                ),

                classes="player-box"
            ),
        )

        #Helps to log and display the options that are chosen by the players
        yield RichLog(id="text_bubble", max_lines=5, auto_scroll=True)


    def on_mount(self):
        """Runs when the app starts. Initializes states."""
        #Helps to loop between player 1 and 2
        self.turn = 0
        
        # Set initial values on progress bars
        self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
        self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
        
        # Welcome message
        log = self.query_one("#text_bubble", RichLog)
        log.write(Text.from_markup("Welcome to [bold yellow]TEXT FIGHTER![/bold yellow]"))
        log.write(Text.from_markup("[bold blue]Use the buttons above or the following keybinds:[/bold blue] [bold red]'a' --> attack [/bold red]|[bold green] 'h' --> heal [/bold green]"))
        log.write(Text.from_markup("[bold yellow]Players can get wounded from being attacked. This reduces your healing effectiveness."))
        log.write(Text.from_markup("[bold yellow]Players can attain higher levels of attack by using the attack option"))
        log.write(Text.from_markup("[bold cyan]PLAYER 1[/bold cyan] should begin!"))


    #This part focuses on the buttons
    def on_button_pressed(self, event: Button.Pressed):
        log = self.query_one("#text_bubble", RichLog)
        
        if self.turn == 0:
            if event.button.id == "button_attack_p1":
                #Get damage using your probability function and log it
                damage_dealt = attack_prob(self.attack_level_p1)
                self.damage_dealt_logger = damage_dealt

                #Deduct the health
                health_modifier = Health(self.p2_hp)
                self.p2_hp = health_modifier.health_deductor(damage_dealt)

                #Health bar changes
                self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
                log.write(Text.from_markup(f"[bold cyan]Player 1[/bold cyan] dealt [bold yellow]{damage_dealt}[/bold yellow] damage to [b red]Player 2![/b red]"))
                header_update = self.query_one("#p2_health_text", Static)
                header_update.update(f"{self.p2_hp}")
                self.cooldown_p1 = max(0, self.cooldown_p1 - 1) #Reduces cooldown of p1 by 1 each turn till 0


                #Adds level
                if self.attack_level_p1 < 4:
                    result = attack_level_prob()
                    if result == 1:
                        self.levelup_p1 += 1

                        if self.levelup_p1 == 3:
                            self.attack_level_p1 += 1
                            self.levelup_p1 = 0
                            #Level bar changes
                            self.query_one("#level_bar_p1", ProgressBar).progress = self.levelup_p1
                            header_update = self.query_one("#attack_training_p1", Static)
                            header_update.update(f"[bold cyan]\nAttack Level: {self.attack_level_p1} [/bold cyan]")        

                        self.query_one("#level_bar_p1", ProgressBar).progress = self.levelup_p1

    
                if self.cooldown_p1 == 0:
                    self.heal_deductor_p1 = 0
                    header_update = self.query_one("#wounded_p1", Static)
                    header_update.update(f"[bold cyan]Player is not wounded!")
                else:
                    header_update = self.query_one("#wounded_p1", Static)
                    header_update.update(f"[bold cyan]Player is wounded! For {self.cooldown_p1} turns!")

                #Check if player died :(
                if self.p2_hp <= 0:
                    log.write(Text.from_markup("[bold cyan]PLAYER 1 HAS WON!!!![/bold cyan] [b red]Player 2[/b red] has been killed :(. Press [b blue]q[/b blue] to quit"))
                    event.button.disabled = True
                    

                else:
                    #Adds into cooldown
                    if self.damage_dealt_logger >= 3 and self.cooldown_p2 == 0:
                        self.cooldown_p2 += 3 
                        self.heal_deductor_p2 = self.damage_dealt_logger
                        header_update = self.query_one("#wounded_p2", Static)
                        header_update.update(f"[bold red]Player is wounded! For {self.cooldown_p2} turns!")
                        self.turn = 1
                    else:
                        self.turn = 1


            elif event.button.id == "button_heal_p1":
                #How much health gained
                health_gained = heal_prob(self.heal_deductor_p1)
            
                #Add the health
                health_modifier = Health(self.p1_hp)

                #Reduces cooldown of p1 by 1 each turn till 0
                self.cooldown_p1 = max(0, self.cooldown_p1 - 1) 
                if self.cooldown_p1 == 0:
                    self.heal_deductor_p1 = 0
                    header_update = self.query_one("#wounded_p1", Static)
                    header_update.update(f"[bold cyan]Player is not wounded!")
                else:
                    header_update = self.query_one("#wounded_p1", Static)
                    header_update.update(f"[bold cyan]Player is wounded! For {self.cooldown_p1} turns!")

                if health_modifier.health_adder(health_gained) >= 15:
                    self.p1_hp = 15
                    self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
                    log.write(Text.from_markup(f"[b cyan]Player 1's[/b cyan] reached max health. Health restored to:[b green] 15![/b green]"))
                    header_update = self.query_one("#p1_health_text", Static)
                    header_update.update(f"{self.p1_hp}")
                    self.turn = 1

                else:
                    self.p1_hp = health_modifier.health_adder(health_gained)
            
                    #Health bar changes
                    self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
                    log.write(Text.from_markup(f"[b cyan]Player 1[/b cyan] gained [b green]{health_gained}![/b green]"))
                    header_update = self.query_one("#p1_health_text", Static)
                    header_update.update(f"{self.p1_hp}")
                    self.turn = 1
                             
            else:
                log.write(Text.from_markup("Incorrect input! It is [bold cyan]PLAYER 1's[/bold cyan] turn!"))
                
    
        elif self.turn == 1:
            if event.button.id == "button_attack_p2": 
                #Get damage using your probability function and log it
                damage_dealt = attack_prob(self.attack_level_p2)
                self.damage_dealt_logger = damage_dealt


                #Deduct the health
                health_modifier = Health(self.p1_hp)
                self.p1_hp = health_modifier.health_deductor(damage_dealt)
            
                #Health bar changes
                self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
                log.write(Text.from_markup(f"[bold red]Player 2[/bold red]  dealt [bold yellow]{damage_dealt}[/bold yellow] damage to [b cyan]Player 1![/b cyan]"))
                header_update = self.query_one("#p1_health_text", Static)
                header_update.update(f"{self.p1_hp}")

                #Adds level
                if self.attack_level_p2 < 4:
                    result = attack_level_prob()
                    if result == 1:
                        self.levelup_p2 += 1

                        if self.levelup_p2 == 3:
                            self.attack_level_p2 += 1
                            self.levelup_p2 == 0
                            #Level bar changes
                            self.query_one("#level_bar_p2", ProgressBar).progress = 0
                            header_update = self.query_one("#attack_training_p2", Static)
                            header_update.update(f"[bold red]\nAttack Level: {self.attack_level_p2} [/bold red]")        

                        #Level bar changes
                        self.query_one("#level_bar_p2", ProgressBar).progress = self.levelup_p2


                #Reduces cooldown of p1 by 1 each turn till 0
                self.cooldown_p2 = max(0, self.cooldown_p2 - 1) 
                if self.cooldown_p2 == 0:
                    self.heal_deductor_p2 = 0
                    header_update = self.query_one("#wounded_p2", Static)
                    header_update.update(f"[bold red]Player is not wounded!")
                else:
                    header_update = self.query_one("#wounded_p2", Static)
                    header_update.update(f"[bold red]Player is wounded! For {self.cooldown_p2} turns!")


                #Check if player died :(
                if self.p1_hp <= 0:
                    log.write(Text.from_markup("[bold red]PLAYER 2 HAS WON!!!![/bold red] [b cyan]Player 1[/b cyan] has been killed :(. Press [b blue]q[/b blue] to quit"))
                    event.button.disabled = True
    
                else:
                    #Adds into cooldown
                    if self.damage_dealt_logger >= 3 and self.cooldown_p1 == 0:
                        self.cooldown_p1 += 3 
                        self.heal_deductor_p1 = self.damage_dealt_logger
                        header_update = self.query_one("#wounded_p1", Static)
                        header_update.update(f"[bold cyan]Player is wounded! For {self.cooldown_p1} turns!")
                        self.turn = 0
                    else:
                        self.turn = 0


            elif event.button.id == "button_heal_p2":
                #How much health gained
                health_gained = heal_prob(self.heal_deductor_p2)
            
                #Add the health
                health_modifier = Health(self.p2_hp)

                #Reduces cooldown of p1 by 1 each turn till 0
                self.cooldown_p2 = max(0, self.cooldown_p2 - 1) 
                if self.cooldown_p2 == 0:
                    self.heal_deductor_p2 = 0
                    header_update = self.query_one("#wounded_p2", Static)
                    header_update.update(f"[bold red]Player is not wounded!")
                else:
                    header_update = self.query_one("#wounded_p2", Static)
                    header_update.update(f"[bold red]Player is wounded! For {self.cooldown_p2} turns!")


                if health_modifier.health_adder(health_gained) >= 15:
                    self.p2_hp = 15
                    self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
                    log.write(Text.from_markup(f"[b red]Player 2[/b red] reached max health. Health restored to:[b green] 15![/b green]"))
                    header_update = self.query_one("#p2_health_text", Static)
                    header_update.update(f"{self.p2_hp}")
                    self.turn = 0

                else:
                    self.p2_hp = health_modifier.health_adder(health_gained)
                    #Health bar changes
                    self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
                    log.write(Text.from_markup(f"[b red]Player 2[/b red] gained [b green]{health_gained}![/b green]"))
                    header_update = self.query_one("#p2_health_text", Static)
                    header_update.update(f"{self.p2_hp}")
                    self.turn = 0

            else:
                log.write(Text.from_markup("Incorrect input! It is [bold cyan]PLAYER 2's[/bold cyan] turn!"))


    #Gives another option to simply use the key board to play the game USING THE KEYBOARD
    def action_attack(self): 
        log = self.query_one("#text_bubble", RichLog)

        if self.turn == 0:
            damage_dealt = attack_prob(self.attack_level_p1)
            self.damage_dealt_logger = damage_dealt

            #Deduct the health
            health_modifier = Health(self.p2_hp)
            self.p2_hp = health_modifier.health_deductor(damage_dealt)
            
            #Health bar changes
            self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
            log.write(Text.from_markup(f"[bold cyan]Player 1[/bold cyan]  dealt [bold yellow]{damage_dealt}[/bold yellow] damage to [b red]Player 2![/b red]"))
            header_update = self.query_one("#p2_health_text", Static)
            header_update.update(f"{self.p2_hp}")
            self.cooldown_p1 = max(0, self.cooldown_p1 - 1) #Reduces cooldown of p1 by 1 each turn till 0

            #Adds level
            if self.attack_level_p1 < 4:
                result = attack_level_prob()
                if result == 1:
                    self.levelup_p1 += 1

                    if self.levelup_p1 == 3:
                        self.attack_level_p1 += 1
                        self.levelup_p1 = 0
                        #Level bar changes
                        self.query_one("#level_bar_p1", ProgressBar).progress = self.levelup_p1
                        header_update = self.query_one("#attack_training_p1", Static)
                        header_update.update(f"[bold cyan]\nAttack Level: {self.attack_level_p1} [/bold cyan]")        

                    self.query_one("#level_bar_p1", ProgressBar).progress = self.levelup_p1


            if self.cooldown_p1 == 0:
                self.heal_deductor_p1 = 0
                header_update = self.query_one("#wounded_p1", Static)
                header_update.update(f"[bold cyan]Player is not wounded!")
            else:
                header_update = self.query_one("#wounded_p1", Static)
                header_update.update(f"[bold cyan]Player is wounded! For {self.cooldown_p1} turns!")
            
            #Check if player died :(
            if self.p2_hp <= 0:
                log.write(Text.from_markup("[bold cyan]PLAYER 1 HAS WON!!!![/bold cyan] [b red]Player 2[/b red] has been killed :(. Press [b blue]q[/b blue] to quit"))
                
            else:
                #Adds into cooldown
                if self.damage_dealt_logger >= 3 and self.cooldown_p2 == 0:
                    self.cooldown_p2 += 3
                    self.heal_deductor_p2 = self.damage_dealt_logger
                    header_update = self.query_one("#wounded_p2", Static)
                    header_update.update(f"[bold red]Player is wounded! For {self.cooldown_p2} turns!")
                    self.turn = 1
                else:
                    self.turn = 1
                    
        elif self.turn == 1:
            damage_dealt = attack_prob(self.attack_level_p2)
            self.damage_dealt_logger = damage_dealt
            
            #Deduct the health
            health_modifier = Health(self.p1_hp)
            self.p1_hp = health_modifier.health_deductor(damage_dealt)
            
            #Health bar changes
            self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
            log.write(Text.from_markup(f"[bold red]Player 2[/bold red]  dealt [bold yellow]{damage_dealt}[/bold yellow] damage to [b cyan]Player 1![/b cyan]"))
            header_update = self.query_one("#p1_health_text", Static)
            header_update.update(f"{self.p1_hp}")

            #Adds level
            if self.attack_level_p2 < 4:
                result = attack_level_prob()
                if result == 1:
                    self.levelup_p2 += 1

                    if self.levelup_p2 == 3:
                        self.attack_level_p2 += 1
                        self.levelup_p2 = 0
                        #Level bar changes
                        self.query_one("#level_bar_p2", ProgressBar).progress = self.levelup_p2
                        header_update = self.query_one("#attack_training_p2", Static)
                        header_update.update(f"[bold red]\nAttack Level: {self.attack_level_p2} [/bold red]")        

                    #Level bar changes
                    self.query_one("#level_bar_p2", ProgressBar).progress = self.levelup_p2


            #Reduces cooldown of p1 by 1 each turn till 0
            self.cooldown_p2 = max(0, self.cooldown_p2 - 1) 
            if self.cooldown_p2 == 0:
                self.heal_deductor_p2 = 0
                header_update = self.query_one("#wounded_p2", Static)
                header_update.update(f"[bold red]Player is not wounded!")
            else:
                header_update = self.query_one("#wounded_p2", Static)
                header_update.update(f"[bold red]Player is wounded! For {self.cooldown_p2} turns!")

            #Check if player died :(
            if self.p1_hp <= 0:
                log.write(Text.from_markup("[bold red]PLAYER 2 HAS WON!!!![/bold red] [b cyan]Player 1[/b cyan] has been killed :(. Press [b blue]q[/b blue] to quit"))
                
            else:
                #Adds into cooldown
                if self.damage_dealt_logger >= 3 and self.cooldown_p1 == 0:
                    self.cooldown_p1 += 3 
                    self.heal_deductor_p1 = self.damage_dealt_logger
                    header_update = self.query_one("#wounded_p1", Static)
                    header_update.update(f"[bold cyan]Player is wounded! For {self.cooldown_p1} turns!")
                    self.turn = 0
                else:
                    self.turn = 0


    def action_heal(self):
        log = self.query_one("#text_bubble", RichLog)

        if self.turn == 0:
            #How much health gained
            health_gained = heal_prob(self.heal_deductor_p1)
            
            #Add the health
            health_modifier = Health(self.p1_hp)

            #Reduces cooldown of p1 by 1 each turn till 0
            self.cooldown_p1 = max(0, self.cooldown_p1 - 1) 
            if self.cooldown_p1 == 0:
                self.heal_deductor_p1 = 0
                header_update = self.query_one("#wounded_p1", Static)
                header_update.update(f"[bold cyan]Player is not wounded!")
            else:
                header_update = self.query_one("#wounded_p1", Static)
                header_update.update(f"[bold cyan]Player is wounded! For {self.cooldown_p1} turns!")
            

            if health_modifier.health_adder(health_gained) >= 15:
                self.p1_hp = 15
                self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
                log.write(Text.from_markup(f"[b cyan]Player 1's[/b cyan] reached max health. Health restored to:[b green] 15![/b green]"))
                header_update = self.query_one("#p1_health_text", Static)
                header_update.update(f"{self.p1_hp}")
                self.turn = 1

            else:
                self.p1_hp = health_modifier.health_adder(health_gained)
            
                #Health bar changes
                self.query_one("#p1_health", ProgressBar).progress = self.p1_hp
                log.write(Text.from_markup(f"[b cyan]Player 1[/b cyan] gained [b green]{health_gained}![/b green]"))
                header_update = self.query_one("#p1_health_text", Static)
                header_update.update(f"{self.p1_hp}")
                self.turn = 1

        elif self.turn == 1:
            #How much health gained
            health_gained = heal_prob(self.heal_deductor_p2)
            
            #Add the health
            health_modifier = Health(self.p2_hp)

            #Reduces cooldown of p1 by 1 each turn till 0
            self.cooldown_p2 = max(0, self.cooldown_p2 - 1) 
            if self.cooldown_p2 == 0:
                self.heal_deductor_p2 = 0
                header_update = self.query_one("#wounded_p2", Static)
                header_update.update(f"[bold red]Player is not wounded!")
            else:
                header_update = self.query_one("#wounded_p2", Static)
                header_update.update(f"[bold red]Player is wounded! For {self.cooldown_p2} turns!")
            

            if health_modifier.health_adder(health_gained) >= 15:
                self.p2_hp = 15
                self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
                log.write(Text.from_markup(f"[b red]Player 2's[/b red] reached max health. Health restored to:[b green] 15![/b green]"))
                header_update = self.query_one("#p2_health_text", Static)
                header_update.update(f"{self.p2_hp}")
                self.turn = 0

            else:
                self.p2_hp = health_modifier.health_adder(health_gained)
            
                #Health bar changes
                self.query_one("#p2_health", ProgressBar).progress = self.p2_hp
                log.write(Text.from_markup(f"[b red]Player 2[/b red] gained [b green]{health_gained}![/b green]"))
                header_update = self.query_one("#p2_health_text", Static)
                header_update.update(f"{self.p2_hp}")
                self.turn = 0


if __name__ == "__main__":
    app = FightingGame()
    app.run()