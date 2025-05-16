extends Node

var current_level: String = ""
var total_fruits_collected: int = 0
var last_checkpoint_position: Vector2 = Vector2.ZERO
var player_node: CharacterBody2D = null

signal checkpoint_updated(new_position: Vector2)
signal fruit_collected(total: int)

func set_player(p: CharacterBody2D) -> void:
	player_node = p

func fruit_eaten():
	total_fruits_collected += 1
	print("Total de frutas coletadas: ", total_fruits_collected)
	if player_node:
		player_node.global_position = last_checkpoint_position
	emit_signal("fruit_collected", total_fruits_collected)

func update_checkpoint(pos: Vector2):
	last_checkpoint_position = pos
	print("Checkpoint atualizado: ", pos)
	emit_signal("checkpoint_updated", pos)

func change_level(level_path: String):
	print("Mudando para o nível:", level_path)
	current_level = level_path
	get_tree().change_scene_to_file(level_path)

func reset():
	total_fruits_collected = 0
	last_checkpoint_position = Vector2.ZERO
	current_level = ""
