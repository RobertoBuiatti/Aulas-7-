extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var itens: Node2D = $Itens

var num_fruit:int = 0
var initial_position = Vector2(238, 157)

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# percorrer todas as frutas
	for item in itens.get_children():
		if item is Fruit or Fruit_Random:
			item.fruit_eaten.connect(_on_fruit_eaten)
			
	

func _process(delta: float) -> void:
	pass

func _on_fruit_eaten():
	num_fruit += 1
	print("Frutas: ", num_fruit)
	player.global_position = initial_position
