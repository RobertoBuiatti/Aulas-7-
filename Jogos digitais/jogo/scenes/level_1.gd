extends Node2D

@onready var player: Sprite2D = $Player

func _ready() -> void:
	player.position.x = 50
	player.position.y = 50
	
	

func _process(delta: float) -> void:
	#player.position.x += 1
	#player.position.y += 1
	
	var direction_x = Input.get_axis("ui_left", "ui_right")
	player.position.x += direction_x * 5
	if direction_x > 0:
		player.flip_h = false
	elif direction_x < 0:
		player.flip_h = true
		
	var direction_y = Input.get_axis("ui_up", "ui_down")
	player.position.y += direction_y * 5
