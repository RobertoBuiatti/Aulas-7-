extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var itens: Node2D = $Itens
@onready var checkpoints: Node2D = $Checkpoint

var num_fruit:int = 0
var initial_position = Vector2(238, 157)
var checkpoints_num:int = 0


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# percorrer todas as frutas
	for item in itens.get_children():
		if item is Fruit or Fruit_Random:
			item.fruit_eaten.connect(_on_fruit_eaten)
			
	
	for Checkpoint in checkpoints.get_children():
		if Checkpoint is checkpoint:
			Checkpoint.checkpoint_atingido.connect(_check_atualização_posicao)
			

func _process(delta: float) -> void:
	pass

func _on_fruit_eaten():
	num_fruit += 1
	print("Frutas: ", num_fruit)
	player.global_position = initial_position

	
func _check_atualização_posicao(cp: Node2D) -> void:
	checkpoints_num += 1
	print("Checkpoints: ", checkpoints_num)
	initial_position = cp.global_position
