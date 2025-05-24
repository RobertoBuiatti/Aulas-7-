extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var soil: TileMapLayer = $Map/Soil


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	# açao do player
	if Input.is_action_just_pressed("ui_select"):
		var pos = soil.local_to_map( player.global_position )
		soil.set_cell(pos, 1, Vector2i(18,11))
