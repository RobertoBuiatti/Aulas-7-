extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var itens: Node2D = $Itens
@onready var checkpoints: Node2D = $Checkpoint

@onready var hud: CanvasLayer = $HUD
@export var next_level: PackedScene

var num_fruit:int = 0
var total_fruits:int = 0
var initial_position = Vector2(238, 157)
var checkpoints_num:int = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var finish = get_tree().get_first_node_in_group("finish")
	if finish:
		finish.win.connect(_on_win)
	# percorrer todas as frutas
	for item in itens.get_children():
		if item is Fruit or Fruit_Random:
			total_fruits += 1
			item.fruit_eaten.connect(_on_fruit_eaten)
	print("Total de frutas no nível: ", total_fruits)
	
	for Checkpoint in checkpoints.get_children():
		if Checkpoint is checkpoint:
			Checkpoint.checkpoint_atingido.connect(_check_atualização_posicao)
			
	#Colisao de dano
	var dangerous = get_tree().get_nodes_in_group("Damage") # pega todos do grupo
	for danger in dangerous:
		danger.get_parent().take_damage.connect(_on_damage)
			

func _on_win():
	if total_fruits == 0:
		print("todas as frutas coletadas!")
		if next_level:
			get_tree().change_scene_to_packed(next_level)
	else:
		print("colete todas as frutas!")
			

func _process(delta: float) -> void:
	pass

func _on_fruit_eaten(quantity):
	hud.eat_fruit(quantity)
	total_fruits -= 1
	print(total_fruits)
	#player.global_position = initial_position

	
func _on_damage() -> void:
	player.global_position = initial_position
	print("morreu")

func _check_atualização_posicao(cp: Node2D) -> void:
	checkpoints_num += 1
	print("Checkpoints: ", checkpoints_num)
	initial_position = cp.global_position
