extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var itens: Node2D = $Itens

var num_fruit:int = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# percorrer todas as frutas
	for item in itens.get_children():
		if item is Fruit:
			item.fruit_eaten.connect(_on_fruit_eaten)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _on_fruit_eaten():
	num_fruit += 1
