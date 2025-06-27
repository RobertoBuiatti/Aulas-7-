extends StaticBody2D

@onready var animation_player: AnimationPlayer = $AnimationPlayer


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	fallfromtree()


func fallfromtree():
	animation_player.play("fallingfromtree")
	await  get_tree().create_timer(1.5).timeout
	animation_player.play("fade")
	await  get_tree().create_timer(0.3).timeout
	queue_free()
