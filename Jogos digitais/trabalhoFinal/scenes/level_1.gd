extends Node2D

@onready var player_2: CharacterBody2D = $Player/Player2
@onready var itens: Node2D = $Itens

var num_fruit:int = 0
var initial_position = Vector2(701, 287)


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
	player_2.global_position = initial_position
	
	
	
	
