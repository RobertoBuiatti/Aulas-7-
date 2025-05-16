extends Node2D

class_name checkpoint

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var animation_player: AnimationPlayer = $AnimationPlayer

signal checkpoint_atingido
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if not animation_player.is_playing() or animation_player.current_animation != "idle":
		animation_player.play("idle")


func _on_area_2d_body_entered(body: Node2D) -> void:
	checkpoint_atingido.emit(self)
	queue_free()
