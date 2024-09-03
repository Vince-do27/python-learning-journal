**Object Orientated Program**

**Classes**

**Basic Pokemon Game OOP Exercise**<br />
```
class Pokemon:
  def __init__(self, name, pokemon_type, hp, damage):
        self.name = name
        self.pokemon_type = pokemon_type
        self.hp = hp
        self.damage = damage

  def __str__(self):
        return f"{self.name} ({self.pokemon_type}) - HP: {self.hp}, Damage: {self.damage}"

  def attack(self, other_pokemon):
        other_pokemon.hp -= self.damage
        return f"{self.name} attacks {other_pokemon.name} for {self.damage} damage!"

  def is_fainted(self):
        return self.hp <= 0

pikachu = Pokemon("Pikachu", "Electric", 35, 10)
bulbasaur = Pokemon("Bulbasaur", "Grass", 45, 8)

print(pikachu)  # Output: Pikachu (Electric) - HP: 35, Damage: 10
print(bulbasaur.attack(pikachu))  # Output: Bulbasaur attacks Pikachu for 8 damage!
print(f"Pikachu's HP: {pikachu.hp}")  # Output: Pikachu's HP: 27
```
